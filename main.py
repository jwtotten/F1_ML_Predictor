import logging
from analyzers import RaceDataAnalyzer
from predictors import MLPredictor
import numpy as np

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    race_analyzer = RaceDataAnalyzer()
    restart = False
    while True:
        season_choice = race_analyzer.select_season()
        all_race_event_data = race_analyzer.load_all_season_race_info()
        logger.info(f"Loaded data for {race_analyzer.season_choice} season:")
        for events in all_race_event_data[:5]:
            logger.info(f"Round {events.get('RoundNumber')}: {events.get('EventName')}")
        all_race_data = race_analyzer.load_all_race_data(all_race_event_data)

        logger.info("Race data loading complete.")
        race_choice = race_analyzer.select_race()
        restart = race_analyzer.present_tabulated_race_data()
        if not restart:
            break

    linear_model_predictor = MLPredictor()
    race_data_for_lec: list = race_analyzer._season_results_for_driver("LEC")

    race_analyzer.plot_driver_season_results(race_data_for_lec)
    race_analyzer.present_driver_season_results("LEC")

    training_data = race_data_for_lec[0:-2]
    validation_data = race_data_for_lec[-2:]

    print("Training Linear Regression Model...")
    print(f"Training Data: {training_data}")
    linear_model_predictor.train(training_data)
    coefficients = linear_model_predictor.return_model_coefficients()
    print(f"Model Coefficients: {coefficients}")

    ## TODO: Clean the data model to fit the random forest regression input.

    print("Training Random Forest Regression Model...")
    print(f"Training Data: {training_data}")
    linear_model_predictor.train_rf(training_data)
    rf_prediction = linear_model_predictor.return_rf_model_prediction(validation_data)
    print(f"Random Forest Model Prediction: {rf_prediction}")
    print(f"Actual Validation Data: {np.array(validation_data).reshape(-1, 1)}")
