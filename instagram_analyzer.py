import numpy as np
from typing import Dict, List, Any
from sentiment import analyze_sentiment
from clip_analysis import analyze_image_clip, extract_colors
import statistics
from datetime import datetime, timedelta

class InstagramAnalyzer:
    def __init__(self):
        self.brand_keywords = [
            "professional", "aesthetic", "beautiful", "brand consistent", 
            "high quality", "stylish", "elegant", "modern"
        ]
    
    def analyze_profile(self, profile_data: Dict) -> Dict[str, Any]:
        """Complete profile analysis with all metrics"""
        
        posts = profile_data.get('posts', [])
        if not posts:
            return {"error": "No posts found for analysis"}
        
        # Brand consistency analysis
        brand_analysis = self._analyze_brand_consistency(posts)
        
        # Engagement analysis
        engagement_analysis = self._analyze_engagement(posts, profile_data.get('followers', 0))
        
        # Sentiment analysis
        sentiment_analysis = self._analyze_sentiment(posts)
        
        # Posting pattern analysis
        posting_analysis = self._analyze_posting_patterns(posts)
        
        # Generate insights and suggestions
        insights = self._generate_insights(brand_analysis, engagement_analysis, sentiment_analysis)
        suggestions = self._generate_mood_suggestions(brand_analysis, sentiment_analysis)
        
        return {
            "profile": {
                "username": profile_data.get('username'),
                "followers": profile_data.get('followers'),
                "following": profile_data.get('following'),
                "posts_count": len(posts)
            },
            "branding": brand_analysis,
            "engagement": engagement_analysis,
            "sentiment": sentiment_analysis,
            "posting": posting_analysis,
            "insights": insights,
            "mood_suggestions": suggestions,
            "generated_at": datetime.now().isoformat()
        }
    
    def _analyze_brand_consistency(self, posts: List[Dict]) -> Dict:
        """Analyze brand consistency across posts"""
        all_colors = []
        aesthetic_scores = []
        
        for post in posts:
            if post.get('image_url'):
                colors = extract_colors(post['image_url'])
                all_colors.extend(colors)
                
                # Check aesthetic consistency
                aesthetic_score = analyze_image_clip(post['image_url'], "brand consistent aesthetic professional")
                aesthetic_scores.append(aesthetic_score)
        
        # Calculate dominant colors
        color_frequency = {}
        for color in all_colors:
            color_frequency[color] = color_frequency.get(color, 0) + 1
        
        dominant_colors = sorted(color_frequency.keys(), key=lambda x: color_frequency[x], reverse=True)[:5]
        
        # Calculate consistency score
        consistency_score = np.mean(aesthetic_scores) * 100 if aesthetic_scores else 0
        
        return {
            "consistency_score": round(consistency_score, 1),
            "dominant_colors": dominant_colors,
            "color_variance": "Low" if consistency_score > 80 else "Moderate" if consistency_score > 60 else "High",
            "brand_alignment": "Strong" if consistency_score > 75 else "Moderate" if consistency_score > 50 else "Weak"
        }
    
    def _analyze_engagement(self, posts: List[Dict], followers: int) -> Dict:
        """Analyze engagement metrics"""
        if not posts:
            return {"error": "No posts to analyze"}
        
        likes = [post.get('likes', 0) for post in posts]
        comments = [post.get('comments', 0) for post in posts]
        
        avg_likes = statistics.mean(likes) if likes else 0
        avg_comments = statistics.mean(comments) if comments else 0
        
        # Calculate engagement rate
        if followers > 0:
            engagement_rate = ((avg_likes + avg_comments) / followers) * 100
        else:
            engagement_rate = 0
        
        # Determine trend (simple comparison of recent vs older posts)
        recent_engagement = statistics.mean([likes[i] + comments[i] for i in range(min(3, len(posts)))])
        older_engagement = statistics.mean([likes[i] + comments[i] for i in range(max(0, len(posts)-3), len(posts))])
        
        trend = "Increasing" if recent_engagement > older_engagement else "Decreasing" if recent_engagement < older_engagement else "Stable"
        
        return {
            "avg_likes": round(avg_likes),
            "avg_comments": round(avg_comments),
            "engagement_rate": round(engagement_rate, 2),
            "trend": trend
        }
    
    def _analyze_sentiment(self, posts: List[Dict]) -> Dict:
        """Analyze sentiment across posts"""
        sentiments = []
        
        for post in posts:
            caption = post.get('caption', '')
            if caption:
                sentiment_score = analyze_sentiment(caption)
                sentiments.append(sentiment_score)
        
        if not sentiments:
            return {"error": "No captions to analyze"}
        
        avg_sentiment = statistics.mean(sentiments)
        
        # Determine emotional tone
        if avg_sentiment > 0.3:
            emotional_tone = "Very Positive"
        elif avg_sentiment > 0:
            emotional_tone = "Positive"
        elif avg_sentiment > -0.3:
            emotional_tone = "Neutral"
        else:
            emotional_tone = "Negative"
        
        return {
            "overall": round(avg_sentiment, 2),
            "trend": "Positive" if avg_sentiment > 0 else "Negative",
            "emotional_tone": emotional_tone
        }
    
    def _analyze_posting_patterns(self, posts: List[Dict]) -> Dict:
        """Analyze posting patterns and timing"""
        if not posts:
            return {"frequency": "Unknown", "optimal_time": "Unknown", "consistency": "Unknown"}
        
        # Calculate posting frequency (posts per week)
        post_dates = [datetime.fromisoformat(post.get('timestamp', '').replace('Z', '+00:00')) for post in posts if post.get('timestamp')]
        
        if len(post_dates) < 2:
            return {"frequency": "Insufficient data", "optimal_time": "Unknown", "consistency": "Unknown"}
        
        date_range = (max(post_dates) - min(post_dates)).days
        frequency = len(posts) / max(date_range / 7, 1)  # posts per week
        
        # Find optimal posting time
        post_hours = [date.hour for date in post_dates]
        optimal_hour = statistics.mode(post_hours) if post_hours else 12
        
        return {
            "frequency": f"{frequency:.1f} posts/week",
            "optimal_time": f"{optimal_hour:02d}:00",
            "consistency": "Good" if 1 <= frequency <= 5 else "Low" if frequency < 1 else "High"
        }
    
    def _generate_insights(self, brand_analysis: Dict, engagement_analysis: Dict, sentiment_analysis: Dict) -> List[str]:
        """Generate actionable insights"""
        insights = []
        
        # Brand insights
        if brand_analysis.get('consistency_score', 0) > 80:
            insights.append("Excellent brand consistency maintained across posts")
        elif brand_analysis.get('consistency_score', 0) < 60:
            insights.append("Consider improving visual consistency for stronger brand identity")
        
        # Engagement insights
        engagement_rate = engagement_analysis.get('engagement_rate', 0)
        if engagement_rate > 3:
            insights.append("Outstanding engagement rate - well above industry average")
        elif engagement_rate < 1:
            insights.append("Engagement rate below average - consider more interactive content")
        
        # Sentiment insights
        if sentiment_analysis.get('overall', 0) > 0.5:
            insights.append("Very positive audience sentiment - maintain authentic voice")
        elif sentiment_analysis.get('overall', 0) < 0:
            insights.append("Consider adjusting content tone to improve audience sentiment")
        
        return insights
    
    def _generate_mood_suggestions(self, brand_analysis: Dict, sentiment_analysis: Dict) -> List[str]:
        """Generate mood and strategy suggestions"""
        suggestions = []
        
        consistency_score = brand_analysis.get('consistency_score', 0)
        sentiment_score = sentiment_analysis.get('overall', 0)
        
        if consistency_score > 75:
            suggestions.append("Maintain current aesthetic direction - it's working well")
        else:
            suggestions.append("Develop a more cohesive visual style guide")
        
        if sentiment_score > 0.3:
            suggestions.append("Continue with positive, uplifting content themes")
        else:
            suggestions.append("Incorporate more inspirational and positive messaging")
        
        # General suggestions
        suggestions.extend([
            "Experiment with user-generated content to boost engagement",
            "Consider seasonal content adjustments while maintaining brand core",
            "Analyze competitor strategies for inspiration",
            "Plan content themes around trending topics in your niche"
        ])
        
        return suggestions
