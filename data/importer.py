import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from activity.stroke_style import Stroke

date_frame = pd.read_csv("./resources/activities.csv")
root: ET.Element = ET.parse("./resources/export.xml").getroot()

WORKOUT = "Workout"
WORKOUT_EVENT = "WorkoutEvent"
ACTIVITY_SUMMARY = "ActivitySummary"
META_DATA_ENTRY = "MetadataEntry"
SWIMMING_ACTIVITY = "HKWorkoutActivityTypeSwimming"
WORKOUT_ACTIVITY_TYPE = "workoutActivityType"
SWIM_LAP_LENGTH = "HKLapLength"

RECORD = "Record"
RECORD_TYPE_HEART_RATE = "HKQuantityTypeIdentifierHeartRateVariabilitySDNN"
RECORD_STROKE_COUNT = "HKQuantityTypeIdentifierSwimmingStrokeCount"
RECORD_BASE_CALORIE = "HKQuantityTypeIdentifierBasalEnergyBurned"
RECORD_ACTIVE_CALORIE = "HKQuantityTypeIdentifierActiveEnergyBurned"
RECORD_STEPS = "HKQuantityTypeIdentifierStepCount"
RECORD_BMI = "HKQuantityTypeIdentifierBodyMassIndex"
RECORD_BODY_FAT = "HKQuantityTypeIdentifierBodyFatPercentage"
RECORD_ENV_AUDIO_EXPOSURE = "HKQuantityTypeIdentifierEnvironmentalAudioExposure"
RECORD_HEAD_PHONES_AUDIO_EXPOSURE = "HKQuantityTypeIdentifierHeadphoneAudioExposure"

HEART_RATE_VARIABILITY = "HeartRateVariabilityMetadataList"
RECORD_CREATION_DATE = "creationDate"
RECORD_START_DATE = "startDate"
RECORD_END_DATE = "endDate"

CALORIE_ACTIVITY_KEY = "activeEnergyBurned"
DATE_COMPONENT_KEY = "dateComponents"
CALORIES_BURNED_UNIT_KEY = "activeEnergyBurnedUnit"

DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
DATE_FORMAT = '%Y-%m-%d'


def find_records():
    return root.findall(RECORD)


def find_activity_Summaries():
    return root.findall(ACTIVITY_SUMMARY)


def find_workouts():
    return root.findall(WORKOUT)


def gather_workouts() -> pd.DataFrame:
    workouts = []

    for workout in find_workouts():
        workout_row = dict()
        workout_row.update(workout.attrib)
        [workout_row.update({i.attrib['key']: i.attrib['value']}) for i in workout.findall(META_DATA_ENTRY)]
        workouts.append(workout_row)

    return pd.DataFrame(workouts)


def get_swim_activities() -> pd.DataFrame:
    activities = []
    for workout in find_workouts():
        if workout.attrib[WORKOUT_ACTIVITY_TYPE] == SWIMMING_ACTIVITY:
            activity = dict()
            activity['duration'] = float(workout.attrib['duration'])
            activity['duration_unit'] = workout.attrib['durationUnit']
            activity['distance'] = float(workout.attrib['totalDistance'])
            activity['distance_unit'] = workout.attrib['totalDistanceUnit']
            activity['calories'] = float(workout.attrib['totalEnergyBurned'])
            activity['creation_time'] = datetime.strptime(workout.attrib[RECORD_START_DATE].split(" +")[0], DATE_TIME_FORMAT) + timedelta(hours=1)
            activity['start_time'] = datetime.strptime(workout.attrib[RECORD_START_DATE].split(" +")[0], DATE_TIME_FORMAT) + timedelta(hours=1)
            activities.append(activity)
    return pd.DataFrame(activities)


def get_swim_laps() -> pd.DataFrame:
    laps = []
    for workout in find_workouts():
        if workout.attrib[WORKOUT_ACTIVITY_TYPE] == SWIMMING_ACTIVITY:
            lap_length = None

            for meta_data in workout.findall(META_DATA_ENTRY):
                if meta_data.attrib['key'] == SWIM_LAP_LENGTH:
                    lap_length = meta_data.attrib['value']

            for lap_event in workout.findall(WORKOUT_EVENT):
                lap = dict(lap_event.attrib)
                lap['lap_length'] = lap_length
                laps.append(lap)

    return pd.DataFrame(laps)


def gather_activity_summaries() -> pd.DataFrame:
    summaries = []
    for summary in find_activity_Summaries():
        activity_row = dict()
        summary_attributes = summary.attrib
        activity_row['date'] = datetime.strptime(summary_attributes[DATE_COMPONENT_KEY], DATE_FORMAT)
        activity_row['unit'] = summary_attributes[CALORIES_BURNED_UNIT_KEY]
        activity_row[CALORIE_ACTIVITY_KEY] = float(summary_attributes[CALORIE_ACTIVITY_KEY])
        summaries.append(activity_row)

    return pd.DataFrame(summaries)


def get_heart_rates() -> pd.DataFrame:
    heart_rates = []
    for record in find_records():
        if record.attrib['type'] == RECORD_TYPE_HEART_RATE:
            date = datetime.strptime(record.attrib[RECORD_START_DATE].split(" +")[0], DATE_TIME_FORMAT) + timedelta(hours=1)
            for heart_rate_lists in record.findall(HEART_RATE_VARIABILITY):
                for heart_rate in heart_rate_lists:
                    heart_rate_row = dict()
                    time = datetime.strptime(heart_rate.attrib['time'], '%H:%M:%S.%f').time()
                    date = date.replace(hour=time.hour, minute=time.minute, second=time.second, microsecond=time.microsecond)
                    heart_rate_row.update({'date': date})
                    try:
                        heart_rate_row['bpm'] = float(heart_rate.attrib['bpm'])
                    except ValueError:
                        heart_rate_row['bpm'] = -1.
                    heart_rates.append(heart_rate_row)

    return pd.DataFrame(heart_rates)


def get_swim_stroke_counts() -> pd.DataFrame:
    strokes = []
    for record in find_records():
        if record.attrib['type'] == RECORD_STROKE_COUNT:
            stroke_row = dict()

            stroke_row['creation_time'] = datetime.strptime(record.attrib[RECORD_START_DATE].split(" +")[0], DATE_TIME_FORMAT) + timedelta(hours=1)
            stroke_row['start_time'] = datetime.strptime(record.attrib[RECORD_START_DATE].split(" +")[0], DATE_TIME_FORMAT) + timedelta(hours=1)
            stroke_row['end_time'] = datetime.strptime(record.attrib[RECORD_END_DATE].split(" +")[0], DATE_TIME_FORMAT) + timedelta(hours=1)
            stroke_row['lengths'] = record.attrib['value']
            for stroke_data in record.findall(META_DATA_ENTRY):
                stroke_row['style'] = Stroke(int(stroke_data.attrib['value']))
                strokes.append(stroke_row)

    return pd.DataFrame(strokes)


def get_calories_burned() -> pd.DataFrame:
    calorie_events = []
    for record in find_records():
        if record.attrib['type'] in (RECORD_BASE_CALORIE, RECORD_ACTIVE_CALORIE):
            calorie_row = dict()
            calorie_row['unit'] = record.attrib['unit']
            calorie_row['creation_time'] = datetime.strptime(record.attrib[RECORD_START_DATE].split(" +")[0], DATE_TIME_FORMAT) + timedelta(hours=1)
            calorie_row['start_time'] = datetime.strptime(record.attrib[RECORD_START_DATE].split(" +")[0], DATE_TIME_FORMAT) + timedelta(hours=1)
            calorie_row['end_time'] = datetime.strptime(record.attrib[RECORD_END_DATE].split(" +")[0], DATE_TIME_FORMAT) + timedelta(hours=1)
            calorie_row['calories'] = record.attrib['value']

            if (record.attrib['type'] == RECORD_BASE_CALORIE):
                calorie_row['type'] = "base"
            elif (record.attrib['type'] == RECORD_ACTIVE_CALORIE):
                calorie_row['type'] = "active"

            calorie_events.append(calorie_row)

    return pd.DataFrame(calorie_events)


def get_steps() -> pd.DataFrame:
    steps = []
    for record in find_records():
        if record.attrib['type'] == RECORD_STEPS:
            step_row = dict()
            step_row['creation_time'] = datetime.strptime(record.attrib[RECORD_START_DATE].split(" +")[0], DATE_TIME_FORMAT) + timedelta(hours=1)
            step_row['start_time'] = datetime.strptime(record.attrib[RECORD_START_DATE].split(" +")[0], DATE_TIME_FORMAT) + timedelta(hours=1)
            step_row['end_time'] = datetime.strptime(record.attrib[RECORD_END_DATE].split(" +")[0], DATE_TIME_FORMAT) + timedelta(hours=1)
            step_row['steps'] = record.attrib['value']
            steps.append(step_row)

    return pd.DataFrame(steps)


def get_bmis() -> pd.DataFrame:
    bmis = []
    for record in find_records():
        if record.attrib['type'] == RECORD_STEPS:
            bmi_row = dict()
            bmi_row['creation_time'] = datetime.strptime(record.attrib[RECORD_START_DATE].split(" +")[0], DATE_TIME_FORMAT) + timedelta(hours=1)
            bmi_row['start_time'] = datetime.strptime(record.attrib[RECORD_START_DATE].split(" +")[0], DATE_TIME_FORMAT) + timedelta(hours=1)
            bmi_row['end_time'] = datetime.strptime(record.attrib[RECORD_END_DATE].split(" +")[0], DATE_TIME_FORMAT) + timedelta(hours=1)
            bmi_row['bmi'] = record.attrib['value']
            bmis.append(bmi_row)

    return pd.DataFrame(bmis)


def get_body_fats() -> pd.DataFrame:
    fats = []
    for record in find_records():
        if record.attrib['type'] == RECORD_BODY_FAT:
            fat_row = dict()
            fat_row['creation_time'] = datetime.strptime(record.attrib[RECORD_START_DATE].split(" +")[0], DATE_TIME_FORMAT) + timedelta(hours=1)
            fat_row['start_time'] = datetime.strptime(record.attrib[RECORD_START_DATE].split(" +")[0], DATE_TIME_FORMAT) + timedelta(hours=1)
            fat_row['end_time'] = datetime.strptime(record.attrib[RECORD_END_DATE].split(" +")[0], DATE_TIME_FORMAT) + timedelta(hours=1)
            fat_row['unit'] = record.attrib['unit']
            fat_row['fat'] = record.attrib['value']
            fats.append(fat_row)

    return pd.DataFrame(fats)


def get_env_audio_exposure() -> pd.DataFrame:
    exposures = []
    for record in find_records():
        if record.attrib['type'] == RECORD_ENV_AUDIO_EXPOSURE:
            exposure_row = dict()
            exposure_row['creation_time'] = datetime.strptime(record.attrib[RECORD_START_DATE].split(" +")[0], DATE_TIME_FORMAT) + timedelta(hours=1)
            exposure_row['start_time'] = datetime.strptime(record.attrib[RECORD_START_DATE].split(" +")[0], DATE_TIME_FORMAT) + timedelta(hours=1)
            exposure_row['end_time'] = datetime.strptime(record.attrib[RECORD_END_DATE].split(" +")[0], DATE_TIME_FORMAT) + timedelta(hours=1)
            exposure_row['unit'] = record.attrib['unit']
            exposure_row['amount'] = record.attrib['value']
            exposures.append(exposure_row)

    return pd.DataFrame(exposures)


def get_phones_audio_exposure() -> pd.DataFrame:
    exposures = []
    for record in find_records():
        if record.attrib['type'] == RECORD_HEAD_PHONES_AUDIO_EXPOSURE:
            exposure_row = dict()
            exposure_row['creation_time'] = datetime.strptime(record.attrib[RECORD_START_DATE].split(" +")[0], DATE_TIME_FORMAT) + timedelta(hours=1)
            exposure_row['start_time'] = datetime.strptime(record.attrib[RECORD_START_DATE].split(" +")[0], DATE_TIME_FORMAT) + timedelta(hours=1)
            exposure_row['end_time'] = datetime.strptime(record.attrib[RECORD_END_DATE].split(" +")[0], DATE_TIME_FORMAT) + timedelta(hours=1)
            exposure_row['unit'] = record.attrib['unit']
            exposure_row['amount'] = record.attrib['value']
            exposures.append(exposure_row)

    return pd.DataFrame(exposures)