#!/usr/bin/env python3
"""
UNFAIR NBA Oracle - Using injuries and advanced stats for predictive edges
"""

from nba_api.stats.endpoints import leaguegamefinder
import pandas as pd

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
    
    # Confidence score based on injury differential
    confidence = max(0.5, min(0.95, (home_adj_pts / max(away_adj_pts, 1)) * 0.7))
    
    return {
        'home_team': home_name,
        'away_team': away_name, 
        'expected_margin': round(expected_margin, 1),
        'confidence': round(confidence, 2),
        'injuries_home': injuries_home,
        'injuries_away': injuries_away,
        'strength': 'UNFAIR' if abs(expected_margin) > 8.0 else 'STRONG' if abs(expected_margin) > 5.0 else 'MODERATE'
    }

# Team IDs
TEAMS = {
    'Lakers': '1610612747',
    'Clippers': '1610612746', 
    'Mavericks': '1610612742',
    'Timberwolves': '1610612750',
    'Nuggets': '1610612743',
    'Trail Blazers': '1610612757',
    'Thunder': '1610612760',
    'Nets': '1610612751',
    'Bucks': '1610612749',
    'Pelicans': '1610612740',
    'Heat': '1610612748',
    'Hawks': '1610612737',
    'Cavaliers': '1610612739',
    'Hornets': '1610612766',
    'Pacers': '1610612754',
    'Wizards': '1610612764',
    'Jazz': '1610612762',
    'Grizzlies': '1610612763'
}

def main():
    print("🏀 UNFAIR NBA ORACLE - INJURY-DRIVEN EDGES")
    print("=" * 60)
    
    # From injury report analysis
    matchups_with_injuries = [
        ('Clippers', 'Lakers', 'Garland/Beal OUT', 'FULL'),
        ('Mavericks', 'Timberwolves', 'Kyrie/Flagg/Gafford OUT', 'FULL'),
        ('Bucks', 'Pelicans', 'Giannis/Turner OUT', 'Trey Murphy OUT'),  
        ('Nuggets', 'Trail Blazers', 'Gordon OUT', 'Lillard OUT+'),
        ('Thunder', 'Nets', 'SGA/JWill OUT', 'Claxton/Williams OUT'),
        ('Cavaliers', 'Hornets', 'Mobley OUT', 'White/Williams OUT'),
        ('Heat', 'Hawks', 'FULL', 'Kuminga OUT'),
        ('Pacers', 'Wizards', 'Siakam/Nembhard OUT', 'TYoung/AD OUT'),
        ('Grizzlies', 'Jazz', 'KCP/Morant OUT', 'Markkanen questionable')
    ]
    
    unfair_picks = []
    
    for matchup in matchups_with_injuries:
        home, away, home_injuries, away_injuries = matchup
        try:
            analysis = unfair_matchup_analysis(
                TEAMS[home], home, 
                TEAMS[away], away,
                home_injuries, away_injuries
            )
            
            print(f"\n📊 {home} vs {away}")
            print(f"   Injuries: {home_injuries} vs {away_injuries}")
            print(f"   Expected Margin: {analysis['expected_margin']} points")
            print(f"   Confidence: {analysis['confidence'] * 100}%")
            print(f"   Strength: {analysis['strength']}")
            
            if analysis['confidence'] >= 0.7:
                unfair_picks.append(analysis)
                
        except Exception as e:
            print(f"Error analyzing {home} vs {away}: {e}")
    
    print("\n" + "=" * 60)
    print("🔥 UNFAIR PICKS TO BET TONIGHT:")
    
    for pick in sorted(unfair_picks, key=lambda x: x['confidence'], reverse=True):
        if pick['expected_margin'] > 0:
            print(f"   🏆 {pick['home_team']} - {pick['expected_margin']} pts (Conf: {pick['confidence'] * 100}%)")
        else:
            print(f"   🏆 {pick['away_team']} +{abs(pick['expected_margin'])} pts (Conf: {pick['confidence'] * 100}%)")

if __name__ == "__main__":
    main()