const anchor = require("@coral-xyz/anchor");
const { Program, AnchorProvider, web3 } = require("@coral-xyz/anchor");
const { Connection, PublicKey } = require("@solana/web3.js");
const { getAssociatedTokenAddress, TOKEN_PROGRAM_ID } = require("@solana/spl-token");
const IDL = require("../target/idl/king_of_the_hill.json");

// Game configuration
const PROGRAM_ID = new PublicKey("Your_Program_ID_Here");
const TOKEN_MINT = new PublicKey("Your_Token_Mint_Here");

class KingOfTheHillClient {
  constructor(connection, wallet) {
    this.connection = connection;
    this.wallet = wallet;
    this.provider = new AnchorProvider(connection, wallet, {
      commitment: "processed",
    });
    this.program = new Program(IDL, PROGRAM_ID, this.provider);
  }

  async getGamePDA() {
    return PublicKey.findProgramAddressSync(
      [Buffer.from("king_of_the_hill"), TOKEN_MINT.toBuffer()],
      PROGRAM_ID
    );
  }

  async getPlayerStatsPDA(player) {
    return PublicKey.findProgramAddressSync(
      [
        Buffer.from("player_stats"),
        player.toBuffer(),
        TOKEN_MINT.toBuffer(),
      ],
      PROGRAM_ID
    );
  }

  async getTreasuryPDA(gamePDA) {
    return PublicKey.findProgramAddressSync(
      [Buffer.from("treasury"), gamePDA.toBuffer()],
      PROGRAM_ID
    );
  }

  async getGameState() {
    const [gamePDA] = await this.getGamePDA();
    try {
      const game = await this.program.account.kingOfTheHill.fetch(gamePDA);
      return {
        currentKing: game.currentKing.toBase58(),
        thronePrice: game.thronePrice.toNumber(),
        totalPot: game.totalPot.toNumber(),
        lastClaimTime: game.lastClaimTime.toNumber(),
        gameEnded: game.gameEnded,
      };
    } catch (e) {
      console.error("Error fetching game state:", e);
      return null;
    }
  }

  async getPlayerStats(player) {
    const [statsPDA] = await this.getPlayerStatsPDA(player);
    try {
      const stats = await this.program.account.playerStats.fetch(statsPDA);
      return {
        wallet: stats.wallet.toBase58(),
        timesKing: stats.timesKing.toNumber(),
        totalEarned: stats.totalEarned.toNumber(),
        totalSpent: stats.totalSpent.toNumber(),
      };
    } catch (e) {
      // Player has no stats yet
      return null;
    }
  }

  async claimThrone() {
    const [gamePDA] = await this.getGamePDA();
    const [statsPDA] = await this.getPlayerStatsPDA(this.wallet.publicKey);
    const [treasuryPDA] = await this.getTreasuryPDA(gamePDA);
    
    const game = await this.program.account.kingOfTheHill.fetch(gamePDA);
    const [prevKingStatsPDA] = await this.getPlayerStatsPDA(game.currentKing);

    const playerTokenAccount = await getAssociatedTokenAddress(
      TOKEN_MINT,
      this.wallet.publicKey
    );

    const prevKingTokenAccount = await getAssociatedTokenAddress(
      TOKEN_MINT,
      game.currentKing
    );

    const tx = await this.program.methods
      .claimThrone()
      .accounts({
        kingOfTheHill: gamePDA,
        player: this.wallet.publicKey,
        playerTokenAccount,
        previousKing: game.currentKing,
        previousKingAccount: prevKingTokenAccount,
        playerStats: statsPDA,
        previousKingStats: prevKingStatsPDA,
        treasury: treasuryPDA,
        tokenMint: TOKEN_MINT,
        tokenProgram: TOKEN_PROGRAM_ID,
        systemProgram: web3.SystemProgram.programId,
        rent: web3.SYSVAR_RENT_PUBKEY,
      })
      .rpc();

    return tx;
  }

  async claimVictory() {
    const [gamePDA] = await this.getGamePDA();
    const [treasuryPDA] = await this.getTreasuryPDA(gamePDA);
    const [winnerStatsPDA] = await this.getPlayerStatsPDA(this.wallet.publicKey);

    const winnerTokenAccount = await getAssociatedTokenAddress(
      TOKEN_MINT,
      this.wallet.publicKey
    );

    const tx = await this.program.methods
      .claimVictory()
      .accounts({
        kingOfTheHill: gamePDA,
        treasury: treasuryPDA,
        treasuryAuthority: treasuryPDA,
        winner: this.wallet.publicKey,
        winnerAccount: winnerTokenAccount,
        winnerStats: winnerStatsPDA,
        tokenMint: TOKEN_MINT,
        tokenProgram: TOKEN_PROGRAM_ID,
      })
      .rpc();

    return tx;
  }

  async startNewRound(initialPrice = 10000000) {
    const [gamePDA] = await this.getGamePDA();
    const [statsPDA] = await this.getPlayerStatsPDA(this.wallet.publicKey);

    const tx = await this.program.methods
      .startNewRound(new anchor.BN(initialPrice))
      .accounts({
        kingOfTheHill: gamePDA,
        initialKing: this.wallet.publicKey,
        newKingStats: statsPDA,
        payer: this.wallet.publicKey,
        tokenMint: TOKEN_MINT,
        systemProgram: web3.SystemProgram.programId,
        rent: web3.SYSVAR_RENT_PUBKEY,
      })
      .rpc();

    return tx;
  }
}

module.exports = { KingOfTheHillClient };
