#!/usr/bin/env python3
"""
UNFAIR NBA Oracle - Tomorrow's Games Analysis (Feb 22)
Using injuries + advanced stats + matchup analysis
"""

from nba_api.stats.endpoints import leaguegamefinder
import pandas as pd
import datetime

def unfair_matchup_analysis(home_team_id, home_name, away_team_id, away_name, injuries_home, injuries_away):
    """Analyze matchups with injury impact weighting"""
    games = leaguegamefinder.LeagueGameFinder(team_id_nullable=home_team_id)
    home_df = games.get_data_frames()[0]
    
    games = leaguegamefinder.LeagueGameFinder(team_id_nullable=away_team_id)  
    away_df = games.get_data_frames()[0]
    
    # Get recent performance
    home_recent = home_df.sort_values('GAME_DATE', ascending=False).head(10)
    away_recent = away_df.sort_values('GAME_DATE', ascending=False).head(10)
    
    # Calculate edges
    home_avg_pts = home_recent['PTS'].mean()
    away_avg_pts = away_recent['PTS'].mean()
    
    # Strength calculations
    home_wins = (home_recent['WL'] == 'W').sum()
    away_wins = (away_recent['WL'] == 'W').sum()
    
    # Injury impact modeling (major star out = -15% scoring)
    injury_factor_home = 1.0 if injuries_home == "FULL" else 0.85
    injury_factor_away = 1.0 if injuries_away == "FULL" else 0.85
    
    # Adjusted scoring expectations
    home_adj_pts = home_avg_pts * injury_factor_home
    away_adj_pts = away_avg_pts * injury_factor_away
    
    # Home court advantage
    home_advantage = 3.0
    
    # Expected margin
    expected_margin = (home_adj_pts + home_advantage) - away_adj_pts
    
    # Confidence score based on injury differential + win percentage
    recent_win_pct_diff = (home_wins - away_wins) / 10.0
    confidence = max(0.5, min(0.95, (home_adj_pts / max(away_adj_pts, 1)) * 0.7 + (recent_win_pct_diff * 0.3)))
    
    return {
        'home_team': home_name,
        'away_team': away_name, 
        'expected_margin': round(expected_margin, 1),
        'confidence': round(confidence, 2),
        'injuries_home': injuries_home,
        'injuries_away': injuries_away,
        'home_win_pct': round((home_wins / 10.0) * 100, 1),
        'away_win_pct': round((away_wins / 10.0) * 100, 1),
        'strength': 'UNFAIR' if abs(expected_margin) > 8.0 else 'STRONG' if abs(expected_margin) > 5.0 else 'MODERATE'
    }

# NBA Team IDs
TEAMS = {
    'Cavaliers': '1610612739',
    'Thunder': '1610612760',
    'Nets': '1610612751',
    'Hawks': '1610612737',
    'Raptors': '1610612761',
    'Bucks': '1610612749',
    'Nuggets': '1610612743',
    'Warriors': '1610612744',
    'Mavericks': '1610612742',
    'Pacers': '1610612754',
    'Hornets': '1610612766',
    'Wizards': '1610612764',
    'Celtics': '1610612738',
    'Lakers': '1610612747',
    '76ers': '1610612755',
    'Timberwolves': '1610612750',
    'Knicks': '1610612752',
    'Bulls': '1610612741',
    'Trail Blazers': '1610612757',
    'Suns': '1610612756',
    'Magic': '1610612753',
    'Clippers': '1610612746'
}

def main():
    print("🏀 UNFAIR NBA ORACLE - TOMORROW'S GAMES (Feb 22)")
    print("=" * 70)
    
    # Tomorrow's key matchups with injury projections
    tomorrow_matchups = [
        ('Thunder', 'Cavaliers', 'SGA/JWill OUT', 'Mobley OUT'),
        ('Hawks', 'Nets', 'Kuminga OUT', 'Claxton/Williams OUT'),
        ('Bucks', 'Raptors', 'Giannis/Turner OUT', 'FULL'),
        ('Warriors', 'Nuggets', 'Curry OUT', 'Gordon OUT'),
        ('Pacers', 'Mavericks', 'Siakam/Nembhard OUT', 'Kyrie/Flagg/Gafford OUT'),
        ('Wizards', 'Hornets', 'TYoung/AD OUT', 'White/Williams OUT'),
        ('Lakers', 'Celtics', 'FULL', 'Tatum OUT'),
        ('Timberwolves', '76ers', 'FULL', 'Embiid OUT'),
        ('Bulls', 'Knicks', 'Collins OUT', 'FULL'),
        ('Suns', 'Trail Blazers', 'Booker questionable', 'Lillard OUT+'),
        ('Clippers', 'Magic', 'Garland/Beal OUT', 'Franz Wagner OUT')
    ]
    
    unfair_picks = []
    
    for matchup in tomorrow_matchups:
        home, away, home_injuries, away_injuries = matchup
        try:
            analysis = unfair_matchup_analysis(
                TEAMS[home], home, 
                TEAMS[away], away,
                home_injuries, away_injuries
            )
            
            print(f"\n📊 {away} @ {home}")
            print(f"   Injuries: {home_injuries} vs {away_injuries}")
            print(f"   Win %: {analysis['home_win_pct']}% vs {analysis['away_win_pct']}%")
            print(f"   Expected Margin: {analysis['home_team']} by {analysis['expected_margin']} pts")
            print(f"   Confidence: {analysis['confidence'] * 100}% ({analysis['strength']})")
            
            if analysis['confidence'] >= 0.65:
                unfair_picks.append(analysis)
                
        except Exception as e:
            print(f"Error analyzing {home} vs {away}: {e}")
    
    print("\n" + "=" * 70)
    print("🔥 UNFAIR PICKS FOR TOMORROW:")
    
    # Sort by confidence
    unfair_picks.sort(key=lambda x: x['confidence'], reverse=True)
    
    for pick in unfair_picks:
        if pick['expected_margin'] > 0:
            print(f"   🏆 {pick['home_team']} - {pick['expected_margin']} pts ({pick['confidence'] * 100}% confidence)")
        else:
            print(f"   🏆 {pick['away_team']} +{abs(pick['expected_margin'])} pts ({pick['confidence'] * 100}% confidence)")
    
    print("\n💎 TOP 3 UNFAIREST PLAYS:")
    for i, pick in enumerate(unfair_picks[:3]):
        print(f"   {i+1}. {pick['home_team'] if pick['expected_margin'] > 0 else pick['away_team']}")

if __name__ == "__main__":
    main()