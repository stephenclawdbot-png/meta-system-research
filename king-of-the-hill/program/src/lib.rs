use anchor_lang::prelude::*;
use anchor_spl::token::{self, Burn, Mint, Token, TokenAccount, Transfer};

declare_id!("Your_Program_ID_Here");

#[program]
pub mod king_of_the_hill {
    use super::*;

    /// Initialize the King of the Hill game
    pub fn initialize_game(
        ctx: Context<InitializeGame>,
        initial_price: u64,
    ) -> Result<()> {
        let king = &mut ctx.accounts.king_of_the_hill;
        let initial_king = ctx.accounts.initial_king.key();
        
        king.current_king = initial_king;
        king.throne_price = initial_price;
        king.total_pot = 0;
        king.last_claim_time = Clock::get()?.unix_timestamp;
        king.game_ended = false;
        king.bump = *ctx.bumps.get("king_of_the_hill").unwrap();
        
        // Initialize player stats for first king
        let player_stats = &mut ctx.accounts.initial_king_stats;
        player_stats.wallet = initial_king;
        player_stats.times_king = 1;
        player_stats.total_earned = 0;
        player_stats.total_spent = 0;
        
        emit!(GameInitialized {
            initial_king,
            initial_price,
            timestamp: king.last_claim_time,
        });
        
        Ok(())
    }

    /// Claim the throne by paying the current price
    pub fn claim_throne(ctx: Context<ClaimThrone>) -> Result<()> {
        let king = &mut ctx.accounts.king_of_the_hill;
        let current_time = Clock::get()?.unix_timestamp;
        
        // Check game hasn't ended (24h timer since last claim)
        let time_since_last = current_time - king.last_claim_time;
        require!(
            !king.game_ended && time_since_last < 86400,
            ErrorCode::GameEnded
        );
        
        let throne_price = king.throne_price;
        let player_key = ctx.accounts.player.key();
        let previous_king = king.current_king;
        
        // Calculate splits:
        // 80% to previous king
        // 15% to pot
        // 5% burn
        let to_previous_king = (throne_price * 80) / 100;
        let to_pot = (throne_price * 15) / 100;
        let to_burn = throne_price - to_previous_king - to_pot; // Remainder to burn
        
        // Pay previous king (80%)
        if previous_king != player_key {
            token::transfer(
                CpiContext::new(
                    ctx.accounts.token_program.to_account_info(),
                    Transfer {
                        from: ctx.accounts.player_token_account.to_account_info(),
                        to: ctx.accounts.previous_king_account.to_account_info(),
                        authority: ctx.accounts.player.to_account_info(),
                    },
                ),
                to_previous_king,
            )?;
            
            // Update previous king's stats - they earned
            let prev_stats = &mut ctx.accounts.previous_king_stats;
            prev_stats.total_earned += to_previous_king;
        }
        
        // Add to pot (15%) - transfer to game treasury
        token::transfer(
            CpiContext::new(
                ctx.accounts.token_program.to_account_info(),
                Transfer {
                    from: ctx.accounts.player_token_account.to_account_info(),
                    to: ctx.accounts.treasury.to_account_info(),
                    authority: ctx.accounts.player.to_account_info(),
                },
            ),
            to_pot,
        )?;
        
        king.total_pot += to_pot;
        
        // Burn tokens (5%)
        token::burn(
            CpiContext::new(
                ctx.accounts.token_program.to_account_info(),
                Burn {
                    mint: ctx.accounts.token_mint.to_account_info(),
                    from: ctx.accounts.player_token_account.to_account_info(),
                    authority: ctx.accounts.player.to_account_info(),
                },
            ),
            to_burn,
        )?;
        
        // Update player's stats - they spent
        let player_stats = &mut ctx.accounts.player_stats;
        player_stats.wallet = player_key;
        player_stats.total_spent += throne_price;
        // times_king will be incremented when they get dethroned and check stats
        
        // Escalate throne price by 10%
        king.throne_price = (king.throne_price * 110) / 100;
        king.current_king = player_key;
        king.last_claim_time = current_time;
        
        emit!(ThroneClaimed {
            new_king: player_key,
            previous_king,
            price_paid: throne_price,
            to_previous_king,
            to_pot,
            burned: to_burn,
            new_price: king.throne_price,
            timestamp: current_time,
        });
        
        Ok(())
    }

    /// Claim victory when 24h has passed with no new claims
    pub fn claim_victory(ctx: Context<ClaimVictory>) -> Result<()> {
        let king = &mut ctx.accounts.king_of_the_hill;
        let current_time = Clock::get()?.unix_timestamp;
        
        let time_since_last = current_time - king.last_claim_time;
        require!(
            time_since_last >= 86400,
            ErrorCode::GameNotEnded
        );
        require!(
            !king.game_ended,
            ErrorCode::AlreadyClaimed
        );
        
        let winner = king.current_king;
        let pot_amount = king.total_pot;
        
        // Transfer pot to winner
        let seeds = &[
            b"treasury",
            king.to_account_info().key.as_ref(),
            &[king.bump],
        ];
        let signer = &[&seeds[..]];
        
        token::transfer(
            CpiContext::new_with_signer(
                ctx.accounts.token_program.to_account_info(),
                Transfer {
                    from: ctx.accounts.treasury.to_account_info(),
                    to: ctx.accounts.winner_account.to_account_info(),
                    authority: ctx.accounts.treasury_authority.to_account_info(),
                },
                signer,
            ),
            pot_amount,
        )?;
        
        // Update winner's stats
        let winner_stats = &mut ctx.accounts.winner_stats;
        winner_stats.total_earned += pot_amount;
        
        king.game_ended = true;
        
        emit!(VictoryClaimed {
            winner,
            amount_won: pot_amount,
            timestamp: current_time,
        });
        
        Ok(())
    }

    /// Start a new game round after someone wins
    pub fn start_new_round(
        ctx: Context<StartNewRound>,
        initial_price: u64,
    ) -> Result<()> {
        let king = &mut ctx.accounts.king_of_the_hill;
        
        require!(
            king.game_ended,
            ErrorCode::GameNotEnded
        );
        
        let initial_king = ctx.accounts.initial_king.key();
        
        king.current_king = initial_king;
        king.throne_price = initial_price;
        king.total_pot = 0;
        king.last_claim_time = Clock::get()?.unix_timestamp;
        king.game_ended = false;
        
        // Initialize player stats
        let player_stats = &mut ctx.accounts.new_king_stats;
        player_stats.wallet = initial_king;
        player_stats.times_king = 1;
        player_stats.total_earned = 0;
        player_stats.total_spent = 0;
        
        emit!(NewRoundStarted {
            initial_king,
            initial_price,
            timestamp: king.last_claim_time,
        });
        
        Ok(())
    }

    /// Update player stats when they become king
    pub fn update_king_stats(ctx: Context<UpdateKingStats>) -> Result<()> {
        let player_stats = &mut ctx.accounts.player_stats;
        player_stats.times_king += 1;
        Ok(())
    }
}

#[derive(Accounts)]
pub struct InitializeGame<'info> {
    #[account(
        init,
        payer = payer,
        space = 8 + KingOfTheHill::SIZE,
        seeds = [b"king_of_the_hill", token_mint.key().as_ref()],
        bump
    )]
    pub king_of_the_hill: Account<'info, KingOfTheHill>,
    
    #[account(
        init,
        payer = payer,
        space = 8 + PlayerStats::SIZE,
        seeds = [b"player_stats", initial_king.key().as_ref(), token_mint.key().as_ref()],
        bump
    )]
    pub initial_king_stats: Account<'info, PlayerStats>,
    
    pub token_mint: Account<'info, Mint>,
    /// CHECK: This is the first king
    pub initial_king: AccountInfo<'info>,
    
    #[account(mut)]
    pub payer: Signer<'info>,
    
    pub system_program: Program<'info, System>,
    pub rent: Sysvar<'info, Rent>,
}

#[derive(Accounts)]
pub struct ClaimThrone<'info> {
    #[account(
        mut,
        seeds = [b"king_of_the_hill", token_mint.key().as_ref()],
        bump = king_of_the_hill.bump,
    )]
    pub king_of_the_hill: Account<'info, KingOfTheHill>,
    
    #[account(mut)]
    pub player: Signer<'info>,
    
    #[account(
        mut,
        token::mint = token_mint,
        token::authority = player,
    )]
    pub player_token_account: Account<'info, TokenAccount>,
    
    /// CHECK: Previous king's wallet
    #[account(
        mut,
        constraint = previous_king.key() == king_of_the_hill.current_king
    )]
    pub previous_king: AccountInfo<'info>,
    
    #[account(
        mut,
        token::mint = token_mint,
        token::authority = previous_king,
    )]
    pub previous_king_account: Account<'info, TokenAccount>,
    
    #[account(
        init_if_needed,
        payer = player,
        space = 8 + PlayerStats::SIZE,
        seeds = [b"player_stats", player.key().as_ref(), token_mint.key().as_ref()],
        bump
    )]
    pub player_stats: Account<'info, PlayerStats>,
    
    #[account(
        mut,
        seeds = [b"player_stats", previous_king.key().as_ref(), token_mint.key().as_ref()],
        bump
    )]
    pub previous_king_stats: Account<'info, PlayerStats>,
    
    #[account(
        mut,
        seeds = [b"treasury", king_of_the_hill.key().as_ref()],
        bump = king_of_the_hill.bump,
    )]
    pub treasury: Account<'info, TokenAccount>,
    
    pub token_mint: Account<'info, Mint>,
    pub token_program: Program<'info, Token>,
    pub system_program: Program<'info, System>,
    pub rent: Sysvar<'info, Rent>,
}

#[derive(Accounts)]
pub struct ClaimVictory<'info> {
    #[account(
        mut,
        seeds = [b"king_of_the_hill", token_mint.key().as_ref()],
        bump = king_of_the_hill.bump,
    )]
    pub king_of_the_hill: Account<'info, KingOfTheHill>,
    
    #[account(
        mut,
        seeds = [b"treasury", king_of_the_hill.key().as_ref()],
        bump = king_of_the_hill.bump,
    )]
    pub treasury: Account<'info, TokenAccount>,
    
    /// CHECK: Treasury authority PDA
    #[account(
        seeds = [b"treasury", king_of_the_hill.key().as_ref()],
        bump = king_of_the_hill.bump,
    )]
    pub treasury_authority: AccountInfo<'info>,
    
    /// CHECK: Current winner (must be current king)
    #[account(
        constraint = winner.key() == king_of_the_hill.current_king
    )]
    pub winner: AccountInfo<'info>,
    
    #[account(
        mut,
        token::mint = token_mint,
        token::authority = winner,
    )]
    pub winner_account: Account<'info, TokenAccount>,
    
    #[account(
        mut,
        seeds = [b"player_stats", winner.key().as_ref(), token_mint.key().as_ref()],
        bump
    )]
    pub winner_stats: Account<'info, PlayerStats>,
    
    pub token_mint: Account<'info, Mint>,
    pub token_program: Program<'info, Token>,
}

#[derive(Accounts)]
pub struct StartNewRound<'info> {
    #[account(
        mut,
        seeds = [b"king_of_the_hill", token_mint.key().as_ref()],
        bump = king_of_the_hill.bump,
    )]
    pub king_of_the_hill: Account<'info, KingOfTheHill>,
    
    /// CHECK: New initial king
    pub initial_king: AccountInfo<'info>,
    
    #[account(
        init_if_needed,
        payer = payer,
        space = 8 + PlayerStats::SIZE,
        seeds = [b"player_stats", initial_king.key().as_ref(), token_mint.key().as_ref()],
        bump
    )]
    pub new_king_stats: Account<'info, PlayerStats>,
    
    #[account(mut)]
    pub payer: Signer<'info>,
    
    pub token_mint: Account<'info, Mint>,
    pub system_program: Program<'info, System>,
    pub rent: Sysvar<'info, Rent>,
}

#[derive(Accounts)]
pub struct UpdateKingStats<'info> {
    #[account(
        mut,
        seeds = [b"player_stats", player.key().as_ref(), token_mint.key().as_ref()],
        bump
    )]
    pub player_stats: Account<'info, PlayerStats>,
    
    pub player: Signer<'info>,
    pub token_mint: Account<'info, Mint>,
}

#[account]
pub struct KingOfTheHill {
    pub current_king: Pubkey,
    pub throne_price: u64,
    pub total_pot: u64,
    pub last_claim_time: i64,
    pub game_ended: bool,
    pub bump: u8,
}

impl KingOfTheHill {
    pub const SIZE: usize = 32 + 8 + 8 + 8 + 1 + 1;
}

#[account]
pub struct PlayerStats {
    pub wallet: Pubkey,
    pub times_king: u64,
    pub total_earned: u64,
    pub total_spent: u64,
}

impl PlayerStats {
    pub const SIZE: usize = 32 + 8 + 8 + 8;
}

#[error_code]
pub enum ErrorCode {
    #[msg("Game has already ended")]
    GameEnded,
    #[msg("Game has not ended yet")]
    GameNotEnded,
    #[msg("Victory already claimed")]
    AlreadyClaimed,
    #[msg("Insufficient token balance")]
    InsufficientBalance,
    #[msg("Not authorized")]
    NotAuthorized,
    #[msg("Invalid account")]
    InvalidAccount,
}

#[event]
pub struct GameInitialized {
    pub initial_king: Pubkey,
    pub initial_price: u64,
    pub timestamp: i64,
}

#[event]
pub struct ThroneClaimed {
    pub new_king: Pubkey,
    pub previous_king: Pubkey,
    pub price_paid: u64,
    pub to_previous_king: u64,
    pub to_pot: u64,
    pub burned: u64,
    pub new_price: u64,
    pub timestamp: i64,
}

#[event]
pub struct VictoryClaimed {
    pub winner: Pubkey,
    pub amount_won: u64,
    pub timestamp: i64,
}

#[event]
pub struct NewRoundStarted {
    pub initial_king: Pubkey,
    pub initial_price: u64,
    pub timestamp: i64,
}
