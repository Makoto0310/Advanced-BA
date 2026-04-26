"""
Conflict Resilience Forecasting Model
Uses machine learning to predict how markets will respond to future geopolitical conflicts
"""
import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split, TimeSeriesSplit
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'config'))
sys.path.insert(0, os.path.dirname(__file__))

from config import *
from utils import *

class ConflictResilienceForecaster:
    """Machine learning model to forecast market resilience during conflicts"""

    def __init__(self, market_data):
        self.market_data = market_data
        self.models = {}
        self.scalers = {}
        self.feature_importance = {}

    def create_historical_features(self, war_events):
        """Create feature matrix from historical conflict data"""

        features_list = []

        for war_name, war_date in war_events.items():
            war_idx = np.argmin(np.abs(self.market_data.index.values.astype('datetime64[D]') - np.datetime64(war_date.date())))

            # Skip if war date is too close to data boundaries
            if war_idx < 30 or war_idx > len(self.market_data) - 30:
                continue

            # Pre-war market conditions (30 days before)
            pre_war_data = self.market_data.iloc[war_idx-30:war_idx]

            # War period performance (30 days after)
            war_period_data = self.market_data.iloc[war_idx:war_idx+30]

            for ticker in RESILIENCE_FOCUS_SECTORS:
                if ticker in self.market_data.columns and not pre_war_data[ticker].isna().all():

                    # Calculate resilience score (30-day recovery)
                    start_price = self.market_data[ticker].iloc[war_idx]
                    end_price = self.market_data[ticker].iloc[min(war_idx+30, len(self.market_data)-1)]

                    if not pd.isna(start_price) and not pd.isna(end_price) and start_price != 0:
                        resilience_score = (end_price - start_price) / start_price * 100

                        # Extract features
                        features = {
                            'war_name': war_name,
                            'ticker': ticker,
                            'resilience_score': resilience_score,
                            'war_year': war_date.year,
                            'war_month': war_date.month,
                            'days_since_epoch': (war_date - pd.Timestamp('2000-01-01')).days,
                        }

                        # Pre-war market conditions
                        if len(pre_war_data) > 0:
                            features.update({
                                'pre_war_volatility': pre_war_data[ticker].pct_change().std() * np.sqrt(252),
                                'pre_war_trend': (pre_war_data[ticker].iloc[-1] - pre_war_data[ticker].iloc[0]) / pre_war_data[ticker].iloc[0] * 100,
                                'pre_war_volume': pre_war_data[ticker].count(),  # proxy for data completeness
                            })

                        # Market-wide conditions
                        if 'SPY' in pre_war_data.columns:
                            features['market_trend'] = (pre_war_data['SPY'].iloc[-1] - pre_war_data['SPY'].iloc[0]) / pre_war_data['SPY'].iloc[0] * 100

                        if '^VIX' in pre_war_data.columns:
                            features['fear_index_avg'] = pre_war_data['^VIX'].mean()

                        # Conflict type indicators (simplified)
                        features.update({
                            'is_middle_east': 1 if 'iraq' in war_name.lower() or 'iran' in war_name.lower() or 'israel' in war_name.lower() else 0,
                            'is_oil_related': 1 if 'iran' in war_name.lower() or 'iraq' in war_name.lower() else 0,
                            'is_recent': 1 if war_date.year >= 2020 else 0,
                        })

                        features_list.append(features)

        return pd.DataFrame(features_list)

    def train_models(self, features_df):
        """Train multiple ML models for resilience prediction"""

        feature_cols = [col for col in features_df.columns if col not in ['war_name', 'ticker', 'resilience_score']]
        self.feature_cols = feature_cols

        models = {
            'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
            'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, random_state=42),
            'Linear Regression': LinearRegression()
        }

        aggregated_results = {name: {'mae': [], 'rmse': [], 'r2': []} for name in models}
        results = {name: {} for name in models}

        for ticker in RESILIENCE_FOCUS_SECTORS:
            ticker_df = features_df[features_df['ticker'] == ticker]
            if len(ticker_df) < 2:
                continue

            X = ticker_df[feature_cols].fillna(ticker_df[feature_cols].mean())
            y = ticker_df['resilience_score']

            if len(X) < 2:
                continue

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
            scaler = StandardScaler().fit(X_train)
            X_train_scaled = scaler.transform(X_train)
            X_test_scaled = scaler.transform(X_test)

            self.scalers[ticker] = scaler
            self.models[ticker] = {}

            for name, model in models.items():
                model_clone = model.__class__(**model.get_params())
                model_clone.fit(X_train_scaled, y_train)
                y_pred = model_clone.predict(X_test_scaled)

                mae = mean_absolute_error(y_test, y_pred)
                rmse = np.sqrt(mean_squared_error(y_test, y_pred))
                r2 = r2_score(y_test, y_pred)

                aggregated_results[name]['mae'].append(mae)
                aggregated_results[name]['rmse'].append(rmse)
                aggregated_results[name]['r2'].append(r2)

                self.models[ticker][name] = model_clone

                if hasattr(model_clone, 'feature_importances_'):
                    if name not in self.feature_importance:
                        self.feature_importance[name] = np.zeros(len(feature_cols))
                    self.feature_importance[name] += model_clone.feature_importances_

        for name in models:
            valid_count = len(aggregated_results[name]['mae'])
            if valid_count > 0:
                results[name] = {
                    'model': None,
                    'mae': np.mean(aggregated_results[name]['mae']),
                    'rmse': np.mean(aggregated_results[name]['rmse']),
                    'r2': np.mean(aggregated_results[name]['r2'])
                }
                if name in self.feature_importance:
                    self.feature_importance[name] /= valid_count

        return results

    def predict_future_resilience(self, future_conflicts, best_model_name='Random Forest'):
        """Predict resilience for hypothetical future conflicts"""

        predictions = []
        for conflict in future_conflicts:
            conflict_features = {
                'war_year': conflict['year'],
                'war_month': conflict['month'],
                'days_since_epoch': (pd.Timestamp(f"{conflict['year']}-{conflict['month']:02d}-01") - pd.Timestamp('2000-01-01')).days,
                'pre_war_volatility': conflict.get('expected_volatility', 0.25),
                'pre_war_trend': conflict.get('market_trend', 0),
                'pre_war_volume': 30,
                'market_trend': conflict.get('market_trend', 0),
                'fear_index_avg': conflict.get('vix_level', 20),
                'is_middle_east': 1 if conflict.get('region') == 'middle_east' else 0,
                'is_oil_related': 1 if conflict.get('involves_oil', False) else 0,
                'is_recent': 1,
            }

            # Convert to DataFrame
            features_df = pd.DataFrame([conflict_features])[self.feature_cols]
            features_df = features_df.fillna(features_df.mean())

            ticker_predictions = {}
            for ticker in RESILIENCE_FOCUS_SECTORS:
                if ticker in self.models and best_model_name in self.models[ticker]:
                    scaler = self.scalers[ticker]
                    features_scaled = scaler.transform(features_df)
                    prediction = self.models[ticker][best_model_name].predict(features_scaled)[0]
                    ticker_predictions[ticker] = prediction

            predictions.append({
                'conflict_name': conflict['name'],
                'predictions': ticker_predictions,
                'features': conflict_features
            })

        return predictions

    def create_forecast_visualizations(self, historical_features, model_results, future_predictions):
        """Create comprehensive forecasting visualizations"""

        print("🎨 Generating forecast visualizations...")

        # 1. Model Performance Comparison
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))

        model_names = list(model_results.keys())
        mae_scores = [model_results[name]['mae'] for name in model_names]
        rmse_scores = [model_results[name]['rmse'] for name in model_names]
        r2_scores = [model_results[name]['r2'] for name in model_names]

        axes[0].bar(model_names, mae_scores, color='skyblue', alpha=0.8)
        axes[0].set_title('Model Performance - MAE', fontweight='bold')
        axes[0].set_ylabel('Mean Absolute Error (%)')
        axes[0].tick_params(axis='x', rotation=45)

        axes[1].bar(model_names, rmse_scores, color='lightcoral', alpha=0.8)
        axes[1].set_title('Model Performance - RMSE', fontweight='bold')
        axes[1].set_ylabel('Root Mean Squared Error (%)')
        axes[1].tick_params(axis='x', rotation=45)

        axes[2].bar(model_names, r2_scores, color='lightgreen', alpha=0.8)
        axes[2].set_title('Model Performance - R²', fontweight='bold')
        axes[2].set_ylabel('R² Score')
        axes[2].tick_params(axis='x', rotation=45)

        plt.tight_layout()
        save_figure(fig, 'forecast_model_performance.png')

        # 2. Feature Importance (Random Forest)
        if 'Random Forest' in self.feature_importance:
            fig, ax = plt.subplots(figsize=(12, 8))

            importance_data = self.feature_importance['Random Forest']
            if isinstance(importance_data, np.ndarray):
                features = self.feature_cols
                importance = importance_data.tolist()
            else:
                features = list(importance_data.keys())
                importance = list(importance_data.values())

            sorted_idx = np.argsort(importance)
            features_sorted = [features[i] for i in sorted_idx]
            importance_sorted = [importance[i] for i in sorted_idx]

            ax.barh(features_sorted, importance_sorted, color='teal', alpha=0.8)
            ax.set_title('Feature Importance - Random Forest Model', fontweight='bold')
            ax.set_xlabel('Importance Score')

            plt.tight_layout()
            save_figure(fig, 'forecast_feature_importance.png')

        # 3. Future Conflict Predictions
        if future_predictions:
            fig, ax = plt.subplots(figsize=(14, 8))

            conflicts = [p['conflict_name'] for p in future_predictions]
            x = np.arange(len(conflicts))
            width = 0.15

            for i, ticker in enumerate(['SPY', 'XLE', 'USO', 'GLD', 'ITA']):
                predictions = [p['predictions'].get(ticker, 0) for p in future_predictions]
                ax.bar(x + i*width, predictions, width, label=ticker, alpha=0.8)

            ax.set_title('Predicted Resilience Scores for Future Conflicts', fontweight='bold')
            ax.set_ylabel('Predicted 30-Day Recovery (%)')
            ax.set_xticks(x + width*2)
            ax.set_xticklabels(conflicts, rotation=45)
            ax.axhline(y=0, color='black', linestyle='--', alpha=0.5)
            ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            ax.grid(True, alpha=0.3)

            plt.tight_layout()
            save_figure(fig, 'future_conflict_predictions.png')

        # 4. Historical vs Predicted Resilience
        fig, ax = plt.subplots(figsize=(12, 8))

        # Historical data
        historical_by_ticker = {}
        for ticker in RESILIENCE_FOCUS_SECTORS:
            ticker_data = historical_features[historical_features['ticker'] == ticker]
            if not ticker_data.empty:
                historical_by_ticker[ticker] = ticker_data['resilience_score'].mean()

        # Future predictions (averaged across conflicts)
        future_by_ticker = {}
        for ticker in RESILIENCE_FOCUS_SECTORS:
            predictions = [p['predictions'].get(ticker, 0) for p in future_predictions]
            if predictions:
                future_by_ticker[ticker] = np.mean(predictions)

        tickers = list(historical_by_ticker.keys())
        hist_scores = [historical_by_ticker[t] for t in tickers]
        fut_scores = [future_by_ticker.get(t, 0) for t in tickers]

        x = np.arange(len(tickers))
        width = 0.35

        ax.bar(x - width/2, hist_scores, width, label='Historical Average', color='steelblue', alpha=0.8)
        ax.bar(x + width/2, fut_scores, width, label='Future Predictions', color='orange', alpha=0.8)

        ax.set_title('Historical vs Predicted Sector Resilience', fontweight='bold')
        ax.set_ylabel('30-Day Recovery (%)')
        ax.set_xticks(x)
        ax.set_xticklabels(tickers)
        ax.axhline(y=0, color='black', linestyle='--', alpha=0.5)
        ax.legend()
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        save_figure(fig, 'historical_vs_predicted_resilience.png')

def main():
    """Main forecasting function"""
    print_analysis_header("Conflict Resilience Forecasting")

    try:
        # Load market data
        market_data = load_market_data()

        # Initialize forecaster
        forecaster = ConflictResilienceForecaster(market_data)

        # Define historical wars for training
        historical_wars = {
            'iraq_war': pd.to_datetime('2003-03-20'),
            'israel_gaza_war': pd.to_datetime('2023-10-07'),
            'us_israel_iran_conflict': pd.to_datetime('2026-02-06')
        }

        print(f"📊 Training on {len(historical_wars)} historical conflicts")

        # Create training features
        features_df = forecaster.create_historical_features(historical_wars)
        print(f"✓ Created {len(features_df)} training samples")

        if len(features_df) < 10:
            print("⚠️  Warning: Limited training data. Results may be unreliable.")
            return

        # Train models
        model_results = forecaster.train_models(features_df)

        print("\n🤖 Model Performance:")
        for name, results in model_results.items():
            print(f"  {name}: MAE={results['mae']:.2f}%, RMSE={results['rmse']:.2f}%, R²={results['r2']:.3f}")
        # Select best model (lowest MAE)
        best_model = min(model_results.items(), key=lambda x: x[1]['mae'])
        print(f"\n🏆 Best Model: {best_model[0]} (MAE: {best_model[1]['mae']:.2f}%)")

        # Define future conflict scenarios
        future_conflicts = [
            {
                'name': 'Red Sea Crisis 2027',
                'year': 2027,
                'month': 6,
                'region': 'middle_east',
                'involves_oil': True,
                'expected_volatility': 0.35,
                'market_trend': -2.0,
                'vix_level': 25
            },
            {
                'name': 'South China Sea 2028',
                'year': 2028,
                'month': 3,
                'region': 'asia',
                'involves_oil': False,
                'expected_volatility': 0.30,
                'market_trend': 1.5,
                'vix_level': 18
            },
            {
                'name': 'Eastern Europe 2029',
                'year': 2029,
                'month': 9,
                'region': 'europe',
                'involves_oil': True,
                'expected_volatility': 0.40,
                'market_trend': -3.5,
                'vix_level': 30
            }
        ]

        print(f"\n🔮 Forecasting resilience for {len(future_conflicts)} future scenarios")

        # Generate predictions
        future_predictions = forecaster.predict_future_resilience(future_conflicts, best_model[0])

        # Create visualizations
        forecaster.create_forecast_visualizations(features_df, model_results, future_predictions)

        # Generate forecast report
        report_path = generate_forecast_report(model_results, future_predictions, features_df)
        print(f"✓ Forecast report saved: {report_path}")

        print("\n" + "="*80)
        print("✅ CONFLICT RESILIENCE FORECASTING COMPLETE")
        print("="*80)
        print(f"📄 Report: {report_path}")
        print(f"📊 Visualizations saved to: {VISUALIZATIONS_DIR}")
        print("\n🔮 KEY PREDICTIONS:")
        for pred in future_predictions:
            top_performer = max(pred['predictions'].items(), key=lambda x: x[1])
            worst_performer = min(pred['predictions'].items(), key=lambda x: x[1])
            print(f"  {pred['conflict_name']}:")
            print(f"    Best: {top_performer[0]} (+{top_performer[1]:.1f}%)")
            print(f"    Worst: {worst_performer[0]} ({worst_performer[1]:.1f}%)")
    except Exception as e:
        print(f"❌ Error during forecasting: {str(e)}")
        import traceback
        traceback.print_exc()

def generate_forecast_report(model_results, future_predictions, features_df):
    """Generate comprehensive forecast report"""

    os.makedirs(REPORTS_DIR, exist_ok=True)
    report_path = os.path.join(REPORTS_DIR, 'conflict_resilience_forecast_report.txt')

    with open(report_path, 'w') as f:
        f.write("="*80 + "\n")
        f.write("CONFLICT RESILIENCE FORECAST REPORT\n")
        f.write("="*80 + "\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Training Data: {len(features_df)} samples from {len(features_df['war_name'].unique())} conflicts\n\n")

        f.write("MODEL PERFORMANCE\n")
        f.write("-" * 30 + "\n")
        for name, results in model_results.items():
            f.write(f"{name}:\n")
            f.write(f"  MAE: {results['mae']:.2f}%\n")
            f.write(f"  RMSE: {results['rmse']:.2f}%\n")
            f.write(f"  R²: {results['r2']:.3f}\n")
            f.write("\n")

        best_model = min(model_results.items(), key=lambda x: x[1]['mae'])
        f.write(f"BEST MODEL: {best_model[0]} (MAE: {best_model[1]['mae']:.2f}%)\n\n")

        f.write("FUTURE CONFLICT PREDICTIONS\n")
        f.write("-" * 35 + "\n")
        for pred in future_predictions:
            f.write(f"Conflict: {pred['conflict_name']}\n")
            f.write("Predicted 30-Day Recovery by Sector:\n")

            sorted_predictions = sorted(pred['predictions'].items(), key=lambda x: x[1], reverse=True)
            for ticker, score in sorted_predictions:
                f.write(f"    {ticker}: {score:.1f}%\n")
            f.write("\n")

        f.write("FORECASTING METHODOLOGY\n")
        f.write("-" * 25 + "\n")
        f.write("• Trained on historical conflict data (2003-2026)\n")
        f.write("• Features: Market conditions, conflict type, timing, volatility\n")
        f.write("• Models: Random Forest, Gradient Boosting, Linear Regression\n")
        f.write("• Prediction: 30-day recovery percentage for key sectors\n")
        f.write("• Scenarios: Hypothetical future conflicts with estimated parameters\n\n")

        f.write("LIMITATIONS & ASSUMPTIONS\n")
        f.write("-" * 25 + "\n")
        f.write("• Historical patterns may not predict unprecedented events\n")
        f.write("• Market reactions depend on conflict scale and global context\n")
        f.write("• Predictions are probabilistic, not deterministic\n")
        f.write("• External factors (economy, policy) not fully captured\n\n")

        f.write("="*80 + "\n")
        f.write("END OF FORECAST REPORT\n")
        f.write("="*80 + "\n")

    return report_path

if __name__ == "__main__":
    main()