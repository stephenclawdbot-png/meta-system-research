#!/usr/bin/env python3
"""
NBA Oracle Class - Real-time NBA analysis system
Provides methods for generating morning briefings, live updates, and recaps
"""

from nba_api.stats.endpoints import leaguegamefinder
import pandas as pd
import datetime
import json

class NBAOracle:
    """NBA Oracle analysis system"""
    
    def __init__(self):
        self.teams = {
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
    
    def get_team_performance(self, team_id, team_name, games_to_analyze=10):
        """Get recent performance stats for a team"""
        try:
            games = leaguegamefinder.LeagueGameFinder(team_id_nullable=team_id)
            df = games.get_data_frames()[0]
            
            # Get most recent games
            recent_games = df.sort_values('GAME_DATE', ascending=False).head(games_to_analyze)
            
            avg_points = recent_games['PTS'].mean()
            avg_plus_minus = recent_games['PLUS_MINUS'].mean()
            win_loss = (recent_games['WL'] == 'W').sum()
            
            return {
                'team': team_name,
                'avg_points': round(avg_points, 1),
                'avg_margin': round(avg_plus_minus, 1),
                'recent_wins': win_loss,
                'recent_games': games_to_analyze,
                'win_pct': round((win_loss / games_to_analyze) * 100, 1)
            }
        except Exception as e:
            return {
                'team': team_name,
                'avg_points': 0,
                'avg_margin': 0,
                'recent_wins': 0,
                'recent_games': games_to_analyze,
                'win_pct': 0,
                'error': str(e)
            }
    
    def analyze_matchup(self, home_team_id, home_name, away_team_id, away_name):
        """Analyze a matchup between two teams"""
        home_stats = self.get_team_performance(home_team_id, home_name)
        away_stats = self.get_team_performance(away_team_id, away_name)
        
        # Simple matchup analysis
        home_advantage = 3.0  # Typical home court advantage
        
        # Calculate expected margin
        expected_margin = (home_stats['avg_points'] + home_advantage) - away_stats['avg_points']
        
        return {
            'home_team': home_stats,
            'away_team': away_stats,
            'expected_margin': round(expected_margin, 1),
            'strength_advantage': 'home' if expected_margin > 0 else 'away'
        }
    
    def get_todays_matchups(self):
        """Get today's key matchups"""
        # For March 2nd, 2026 - key matchups
        return [
            ('Lakers', 'Clippers'),
            ('Mavericks', 'Timberwolves'),
            ('Nuggets', 'Trail Blazers'),
            ('Thunder', 'Nets'),
            ('Bucks', 'Pelicans'),
            ('Heat', 'Hawks'),
            ('Cavaliers', 'Hornets'),
            ('Pacers', 'Wizards')
        ]
    
    def generate_morning_briefing(self):
        """Generate morning briefing report"""
        current_time = datetime.datetime.now().strftime("%H:%M GMT+8")
        matchups = self.get_todays_matchups()
        
        report = f"""🏀 NBA ORACLE - MORNING BRIEFING
{'='*50}
📅 {datetime.datetime.now().strftime("%A, %B %d, %Y")}
🕒 {current_time}

🚀 TODAY'S KEY MATCHUPS:

"""
        
        for i, (home, away) in enumerate(matchups[:5], 1):
            try:
                analysis = self.analyze_matchup(self.teams[home], home, self.teams[away], away)
                report += f"{i}. **{home} vs {away}**\n"
                report += f"   Point Spread: {home} {'-' if analysis['expected_margin'] > 0 else '+'}{abs(analysis['expected_margin']):.1f}\n"
                report += f"   Expected Winner: {analysis['strength_advantage'].title()}\n"
                report += f"   Strength: {analysis['expected_margin']:.1f} point advantage\n\n"
            except Exception as e:
                report += f"{i}. **{home} vs {away}** - Analysis unavailable\n\n"
        
        report += """📊 KEY INSIGHTS:
• **Western Conference Showdown**: Lakers vs Clippers rivalry heats up
• **MVP Candidates**: Look for standout performances from top players  
• **Playoff Implications**: Several games with seeding consequences
• **Injury Watch**: Monitor pre-game reports for lineup changes

🎯 BETTING CONSIDERATIONS:
• Home court advantage (~3 points)
• Back-to-back game fatigue factor
• Motivation levels for playoff vs lottery teams
• Recent team performance trends

⚡ Stay locked in for live updates throughout the day!

⚠️ Entertainment and analysis purposes only
"""
        
        return report
    
    def generate_live_updates(self):
        """Generate live updates report"""
        current_time = datetime.datetime.now().strftime("%H:%M GMT+8")
        
        report = f"""🏀 NBA ORACLE - LIVE GAME UPDATES
{'='*50}
📊 LIVE SCORES & ANALYSIS
🕒 {current_time}

🎯 TODAY'S SCORES & LIVE ACTION:

"""
        
        # Simulated live scores for demo
        live_games = [
            ("Lakers", "Clippers", 112, 108, "2:30 remaining", "Close battle"),
            ("Mavericks", "Timberwolves", 98, 102, "Final", "Timberwolves win"),
            ("Nuggets", "Trail Blazers", 115, 98, "4:15 remaining", "Nuggets dominant"),
            ("Thunder", "Nets", 105, 103, "Overtime", "Thriller ending"),
            ("Bucks", "Pelicans", 121, 118, "Final", "Bucks edge it out")
        ]
        
        for home, away, home_score, away_score, status, analysis in live_games:
            report += f"**{home} vs {away}**\n"
            report += f"   Score: {home_score}-{away_score} | Status: {status}\n"
            report += f"   Analysis: {analysis}\n"
            
            if "remaining" in status:
                momentum = "Home team" if home_score > away_score else "Away team"
                report += f"   Momentum: {momentum} controlling the game\n"
            
            report += "\n"
        
        report += """🔥 LIVE BETTING INSIGHTS:
• **Momentum Swings**: Look for teams with strong second halves
• **Player Performance**: Monitor star player usage and efficiency
• **Clutch Factor**: Which teams excel in close game situations
• **In-Game Adjustments**: Coaching decisions impacting outcomes

📈 REAL-TIME METRICS:
• Offensive efficiency ratings
• Defensive pressure intensity
• Turnover differentials
• Rebounding battles

🏆 Stay tuned for more updates throughout the games!

⚠️ Entertainment purposes only - bet responsibly
"""
        
        return report
    
    def get_scoreboard(self):
        """Get today's scoreboard data"""
        # For demo purposes - return mock data
        # In production, this would call the NBA API
        return {
            'events': [
                {
                    'name': 'Los Angeles Lakers vs Los Angeles Clippers',
                    'status': {'type': {'description': 'Scheduled'}},
                    'competitions': [{
                        'competitors': [
                            {'homeAway': 'home', 'team': {'displayName': 'Lakers'}},
                            {'homeAway': 'away', 'team': {'displayName': 'Clippers'}}
                        ],
                        'odds': [{
                            'awayTeamOdds': {'favorite': True},
                            'spread': -4.5,
                            'overUnder': 235.5
                        }]
                    }]
                },
                {
                    'name': 'Dallas Mavericks vs Minnesota Timberwolves',
                    'status': {'type': {'description': 'Scheduled'}},
                    'competitions': [{
                        'competitors': [
                            {'homeAway': 'home', 'team': {'displayName': 'Mavericks'}},
                            {'homeAway': 'away', 'team': {'displayName': 'Timberwolves'}}
                        ],
                        'odds': [{
                            'homeTeamOdds': {'favorite': True},
                            'spread': 2.5,
                            'overUnder': 228.0
                        }]
                    }]
                }
            ]
        }
    
    def generate_evening_recap(self):
        """Generate evening recap report"""
        current_time = datetime.datetime.now().strftime("%H:%M GMT+8")
        
        report = f"""🏀 NBA ORACLE - EVENING RECAP
{'='*50}
📝 TODAY'S NBA ACTION WRAP-UP
🕒 {current_time}

🎯 FINAL RESULTS & ANALYSIS:

"""
        
        # Simulated final results
        final_games = [
            ("Lakers", "Clippers", 112, 108, "Lakers win close rivalry game"),
            ("Mavericks", "Timberwolves", 98, 102, "Timberwolves defense prevails"),
            ("Nuggets", "Trail Blazers", 115, 98, "Nuggets dominate from start"),
            ("Thunder", "Nets", 105, 103, "Thunder win OT thriller"),
            ("Bucks", "Pelicans", 121, 118, "Bucks hold on for victory")
        ]
        
        for home, away, home_score, away_score, analysis in final_games:
            winner = home if home_score > away_score else away
            margin = abs(home_score - away_score)
            report += f"**{home} vs {away}**\n"
            report += f"   Final: {home_score}-{away_score} | {winner} wins by {margin}\n"
            report += f"   Analysis: {analysis}\n\n"
        
        report += """🏆 STANDOUT PERFORMANCES:
• **Player of the Night**: [Top scorer + key stats]
• **Defensive Standout**: [Top defender + impact plays]
• **Rising Star**: [Emerging player making noise]
• **Veteran Leadership**: [Experienced player closing games]

📊 KEY TAKEAWAYS:
• Playoff picture updates
• Injury impacts on team performance
• Coaching decisions that made a difference
• Trends to watch going forward

🎯 LOOKING AHEAD:
• Tomorrow's marquee matchups
• Player milestone watches
• Streak analysis (win/loss trends)
• Betting angles for upcoming games

💡 Oracle Analysis Complete - See you tomorrow!

⚠️ Analysis for entertainment and educational purposes
"""
        
        return report

def main():
    """Test the NBA Oracle class"""
    oracle = NBAOracle()
    
    print("Testing NBA Oracle Class:")
    print("="*50)
    
    print("\n1. Morning Briefing:")
    print(oracle.generate_morning_briefing())
    
    print("\n\n2. Live Updates:")
    print(oracle.generate_live_updates())
    
    print("\n\n3. Evening Recap:")
    print(oracle.generate_evening_recap())

if __name__ == "__main__":
    main()