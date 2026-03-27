#!/usr/bin/env python3
"""
NBA Picks and Analysis System
Advanced analytics and betting recommendations
"""

import json
from datetime import datetime
from nba_oracle import NBAOracle

class NBAPicks:
    def __init__(self):
        self.oracle = NBAOracle()
        self.analysis_cache = {}
    
    def analyze_game_odds(self, game_data):
        """Analyze betting odds and make recommendations"""
        if not game_data or game_data == "No game data available":
            return "No game data available"
        
        picks = []
        for event in game_data['events']:
            game_info = {
                'name': event['name'],
                'status': event['status']['type']['description'],
                'analysis': {},
                'recommendation': {}
            }
            
            # Get game details
            competition = event.get('competitions', [{}])[0]
            competitors = competition.get('competitors', [])
            
            if len(competitors) == 2:
                home_team = competitors[0] if competitors[0]['homeAway'] == 'home' else competitors[1]
                away_team = competitors[1] if competitors[0]['homeAway'] == 'home' else competitors[0]
                
                # Team records
                home_record = home_team.get('records', [{}])[0].get('summary', '')
                away_record = away_team.get('records', [{}])[0].get('summary', '')
                
                # Calculate win percentage
                def win_percentage(record):
                    if '-' in record:
                        try:
                            wins, losses = map(int, record.split('-'))
                            total = wins + losses
                            return wins / total if total > 0 else 0
                        except:
                            return 0
                    return 0
                
                home_win_pct = win_percentage(home_record)
                away_win_pct = win_percentage(away_record)
                
                # Analyze betting odds
                odds_data = competition.get('odds', [])
                for odds in odds_data:
                    if 'details' in odds:
                        # Simple analysis based on records and odds
                        favorite = odds.get('awayTeamOdds', {}).get('favorite', False)
                        underdog = odds.get('homeTeamOdds', {}).get('underdog', False)
                        
                        spread = odds.get('spread', 0)
                        total = odds.get('overUnder', 0)
                        
                        # Make recommendation
                        if favorite:
                            fav_team = away_team['team']['displayName'] if odds.get('awayTeamOdds', {}).get('favorite') else home_team['team']['displayName']
                            game_info['analysis']['favorite'] = f"{fav_team} is favored by {abs(spread)} points"
                            
                            # Value analysis
                            if abs(spread) <= 3.5:
                                game_info['recommendation']['spread'] = f"Consider betting the favorite (small spread)"
                            elif abs(spread) >= 10:
                                game_info['recommendation']['spread'] = f"Consider betting the underdog (large spread)"
                        
                        # Total points analysis
                        if total > 240:
                            game_info['analysis']['total'] = "High-scoring game expected"
                            game_info['recommendation']['total'] = "Consider betting OVER"
                        elif total < 220:
                            game_info['analysis']['total'] = "Low-scoring game expected"
                            game_info['recommendation']['total'] = "Consider betting UNDER"
                
                picks.append(game_info)
        
        return picks
    
    def generate_picks_report(self):
        """Generate comprehensive picks and analysis report"""
        game_data = self.oracle.get_scoreboard()
        picks = self.analyze_game_odds(game_data)
        
        report = "🏀 NBA Picks & Analysis 🏀\n"
        report += f"📊 Generated: {datetime.now().strftime('%A, %B %d, %Y %I:%M %p')}\n\n"
        
        if isinstance(picks, str):
            report += picks
        else:
            report += f"🎯 Game Analysis ({len(picks)} games today):\n\n"
            
            for pick in picks:
                report += f"🏀 {pick['name']}\n"
                report += f"📈 Status: {pick['status']}\n"
                
                if pick['analysis']:
                    report += "🔍 Analysis:\n"
                    for key, analysis in pick['analysis'].items():
                        report += f"   • {analysis}\n"
                
                if pick['recommendation']:
                    report += "💡 Recommendations:\n"
                    for key, rec in pick['recommendation'].items():
                        report += f"   • {rec}\n"
                
                report += "\n"
        
        return report
    
    def generate_gambling_picks(self):
        """Generate specific gambling picks with confidence levels"""
        game_data = self.oracle.get_scoreboard()
        picks = self.analyze_game_odds(game_data)
        
        gambling_picks = "💰 NBA Gambling Picks 💰\n"
        gambling_picks += f"🎲 Generated: {datetime.now().strftime('%A, %B %d, %Y %I:%M %p')}\n\n"
        gambling_picks += "🏆 Top Picks for Today:\n\n"
        
        if isinstance(picks, str):
            gambling_picks += picks
        else:
            high_confidence = []
            medium_confidence = []
            low_confidence = []
            
            for pick in picks:
                if pick['status'].lower() == 'scheduled':
                    # Simple scoring system
                    score = 0
                    
                    # Higher score for more confident picks
                    if 'small spread' in str(pick.get('recommendation', {})):
                        score += 2
                    if 'consider betting' in str(pick.get('recommendation', {})):
                        score += 1
                    
                    if score >= 2:
                        high_confidence.append(pick)
                    elif score == 1:
                        medium_confidence.append(pick)
                    else:
                        low_confidence.append(pick)
            
            if high_confidence:
                gambling_picks += "🔥 HIGH CONFIDENCE PICKS:\n"
                for pick in high_confidence:
                    gambling_picks += f"✅ {pick['name']}\n"
                    for rec in pick.get('recommendation', {}).values():
                        gambling_picks += f"   • {rec}\n"
                gambling_picks += "\n"
            
            if medium_confidence:
                gambling_picks += "📊 MEDIUM CONFIDENCE PICKS:\n"
                for pick in medium_confidence:
                    gambling_picks += f"📈 {pick['name']}\n"
                    for rec in pick.get('recommendation', {}).values():
                        gambling_picks += f"   • {rec}\n"
                gambling_picks += "\n"
            
            if low_confidence:
                gambling_picks += "⚠️  LOW CONFIDENCE PICKS:\n"
                for pick in low_confidence:
                    gambling_picks += f"⚡ {pick['name']}\n"
                    for rec in pick.get('recommendation', {}).values():
                        gambling_picks += f"   • {rec}\n"
                gambling_picks += "\n"
            
            if not any([high_confidence, medium_confidence, low_confidence]):
                gambling_picks += "No strong picks identified for today based on current analysis.\n"
        
        gambling_picks += "\n⚠️  DISCLAIMER: Gambling involves risk. Bet responsibly.\n"
        
        return gambling_picks

def main():
    picks_system = NBAPicks()
    
    print("Testing NBA Picks System...\n")
    
    # Test picks report
    print("=== NBA Picks Report ===")
    report = picks_system.generate_picks_report()
    print(report)
    
    # Test gambling picks
    print("\n=== Gambling Picks ===")
    gambling_picks = picks_system.generate_gambling_picks()
    print(gambling_picks)

if __name__ == "__main__":
    main()