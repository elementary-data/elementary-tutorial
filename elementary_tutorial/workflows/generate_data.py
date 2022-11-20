from collections import defaultdict
from datetime import datetime, timedelta
import hashlib
import os
from pathlib import Path
import random

from elementary_tutorial.utils.csv import split_csv_to_headers_and_data, write_to_csv
from elementary_tutorial.utils.dbt_project import get_seed_file_path


PROJECT_DIR = Path(os.path.dirname(__file__)).parent.absolute()
ORIGINAL_DATA_PATH = os.path.join(PROJECT_DIR, "original_jaffle_shop_data")

CUSTOMERS_COUNT = 300
ORDERS_COUNT = 1500
TIME_SPAN_IN_DAYS = 14
MAX_PAYMENTS_PER_ORDER = 3
LOWEST_PAYMENT_IN_HUNDRENDS = 0
HIGHEST_PAYMENT_IN_HUNDRENDS = 7


def generate_data():
    print("Generate tutorial seed data.")
    generate_customers_data()
    generate_orders_data()
    generate_payments_data()
    generate_signups_data()
    generate_customers_anomalies_data()
    generate_orders_anomalies_data()
    generate_payments_anomalies_data()
    generate_signups_anomlies_data()
    print("Generated tutorial seed data successfully.")


def generate_customers_data():
    original_customers_data_path = os.path.join(ORIGINAL_DATA_PATH, "raw_customers.csv")
    tutorial_customers_data_path = get_seed_file_path("customers_training", "training")
    headers, original_customers_data = split_csv_to_headers_and_data(
        csv_path=original_customers_data_path
    )
    all_first_names = list(set([row[1] for row in original_customers_data]))
    all_last_names = list(set([row[2] for row in original_customers_data]))
    new_customers = []
    for customer_id in range(1, CUSTOMERS_COUNT + 1):
        new_customers.append(
            [
                customer_id,  # CUSTOMER ID
                random.choice(all_first_names),  # FIRST NAME
                random.choice(all_last_names),  # LAST NAME
            ]
        )
    write_to_csv(tutorial_customers_data_path, headers, new_customers)


def generate_orders_data():
    original_orders_data_path = os.path.join(ORIGINAL_DATA_PATH, "raw_orders.csv")
    tutorial_orders_data_path = get_seed_file_path("orders_training", "training")
    headers, original_orders_data = split_csv_to_headers_and_data(
        csv_path=original_orders_data_path
    )
    all_order_statuses = list(set([row[3] for row in original_orders_data]))
    new_orders = []
    for order_id in range(1, ORDERS_COUNT + 1):
        # Make sure we got at least 1 order at each day
        order_datetime = (
            (datetime.now() - timedelta(random.randint(1, TIME_SPAN_IN_DAYS)))
            if order_id > TIME_SPAN_IN_DAYS
            else (datetime.now() - timedelta(random.randint(1, order_id)))
        )
        new_orders.append(
            [
                order_id,  # ORDER ID
                random.randint(1, CUSTOMERS_COUNT),  # CUSTOMER ID
                order_datetime.strftime("%Y-%m-%d"),  # ORDER DATE
                random.choice(all_order_statuses),  # ORDER STATUS
            ]
        )
    write_to_csv(tutorial_orders_data_path, headers, new_orders)


def generate_payments_data():
    original_payments_data_path = os.path.join(ORIGINAL_DATA_PATH, "raw_payments.csv")
    tutorial_payments_data_path = get_seed_file_path("payments_training", "training")
    headers, original_payments_data = split_csv_to_headers_and_data(
        csv_path=original_payments_data_path
    )
    all_payments_methods = list(set([row[2] for row in original_payments_data]))
    new_payments = []
    payment_id = 1
    for order_id in range(1, ORDERS_COUNT + 1):
        amount_of_payments = random.randint(1, MAX_PAYMENTS_PER_ORDER)
        max_total_payment_in_hundrends = HIGHEST_PAYMENT_IN_HUNDRENDS
        for payment in range(amount_of_payments):
            payment_amount_in_hundrends = random.randint(
                LOWEST_PAYMENT_IN_HUNDRENDS, max_total_payment_in_hundrends
            )
            new_payments.append(
                [
                    payment_id,  # PAYMENT_ID
                    order_id,  # ORDER ID
                    random.choice(all_payments_methods),  # PAYMENT METHOD
                    (payment_amount_in_hundrends + 1) * 100,  # AMOUNT
                ]
            )
            payment_id += 1
            max_total_payment_in_hundrends -= payment_amount_in_hundrends
    write_to_csv(tutorial_payments_data_path, headers, new_payments)


def generate_signups_data():
    tutorial_payments_data_path = get_seed_file_path("signups_training", "training")
    headers = ["id", "user_id", "user_email", "hashed_password", "signup_date"]
    tutorial_customers_data_path = get_seed_file_path("customers_training", "training")
    tutorial_orders_data_path = get_seed_file_path("orders_training", "training")
    customers_headers, customers_data = split_csv_to_headers_and_data(
        csv_path=tutorial_customers_data_path
    )
    orders_headers, orders_data = split_csv_to_headers_and_data(
        csv_path=tutorial_orders_data_path
    )

    customer_min_order_time_map = defaultdict(
        lambda: (
            datetime.now() - timedelta(random.randint(1, TIME_SPAN_IN_DAYS))
        ).strftime("%Y-%m-%d")
    )
    for order in orders_data:
        customer_min_order_time_map[order[1]] = min(
            datetime.strptime(customer_min_order_time_map[order[1]], "%Y-%m-%d"),
            datetime.strptime(order[2], "%Y-%m-%d"),
        ).strftime("%Y-%m-%d")

    new_signups = []
    for customer in customers_data:
        new_signups.append(
            [
                customer[0],  # SIGNUP ID
                customer[0],  # CUSTOMER ID
                f"{customer[1]}{customer[2].lower()}{customer[0]}@example.com"
                if random.randint(0, 30)
                else "",  # USER EMAIL
                hashlib.sha256(datetime.now().isoformat().encode()).hexdigest(),
                customer_min_order_time_map[customer[0]],
            ]
        )
    write_to_csv(tutorial_payments_data_path, headers, new_signups)


def generate_customers_anomalies_data():
    # Generate big amount of new customers to create a row count anomaly
    customers_data_path = get_seed_file_path("customers_training", "training")
    customers_anomalies_data_path = get_seed_file_path(
        "customers_validation", "validation"
    )
    headers, customers = split_csv_to_headers_and_data(csv_path=customers_data_path)
    all_first_names = list(set([row[1] for row in customers]))
    all_last_names = list(set([row[2] for row in customers]))
    new_customers = [*customers]
    for customer_id in range(len(customers) + 1, len(customers) + CUSTOMERS_COUNT * 3):
        new_customers.append(
            [
                customer_id,  # CUSTOMER ID
                random.choice(all_first_names),  # FIRST NAME
                random.choice(all_last_names),  # LAST NAME
            ]
        )
    write_to_csv(customers_anomalies_data_path, headers, new_customers)


def generate_orders_anomalies_data():
    # Generate big amount of returned orders to create a dimension anomaly
    orders_data_path = get_seed_file_path("orders_training", "training")
    orders_anomalies_path = get_seed_file_path("orders_validation", "validation")
    orders_headers, orders = split_csv_to_headers_and_data(csv_path=orders_data_path)
    new_orders = [*orders]
    validation_orders_date = (datetime.now() - timedelta(1)).strftime("%Y-%m-%d")
    for order_id in range(len(orders) + 1, len(orders) + ORDERS_COUNT * 3):
        new_orders.append(
            [
                order_id,  # ORDER ID
                random.randint(1, CUSTOMERS_COUNT),  # CUSTOMER ID
                validation_orders_date,  # ORDER DATE
                "returned",  # ORDER STATUS
            ]
        )
    write_to_csv(orders_anomalies_path, orders_headers, new_orders)


def generate_payments_anomalies_data():
    # Generate big amount of payments to create a row count anomaly
    # All new payments have amount of 0 to create a coulumn anomalies of count zero and percent zero
    payments_data_path = get_seed_file_path("payments_training", "training")
    payments_anomalies_data_path = get_seed_file_path(
        "payments_validation", "validation"
    )
    payments_headers, payments = split_csv_to_headers_and_data(
        csv_path=payments_data_path
    )
    all_payments_methods = list(set([row[2] for row in payments]))
    new_payments = [*payments]
    payment_id = len(payments) + 1
    for order_id in range(ORDERS_COUNT + 1, ORDERS_COUNT + ORDERS_COUNT * 3):
        new_payments.append(
            [
                payment_id,  # PAYMENT_ID
                order_id,  # ORDER ID
                random.choice(all_payments_methods),  # PAYMENT METHOD
                0,  # AMOUNT
            ]
        )
        payment_id += 1
    write_to_csv(payments_anomalies_data_path, payments_headers, new_payments)


def generate_signups_anomlies_data():
    # Generate signups for the new customers generated.
    signups_data_path = get_seed_file_path("signups_training", "training")
    signups_anomalies_data_path = get_seed_file_path("signups_validation", "validation")
    customers_anomalies_data_path = get_seed_file_path(
        "customers_validation", "validation"
    )
    customers_headers, customers = split_csv_to_headers_and_data(
        csv_path=customers_anomalies_data_path
    )
    signups_headers, signups = split_csv_to_headers_and_data(csv_path=signups_data_path)

    new_signups = [*signups]
    validation_signup_date = (datetime.now() - timedelta(1)).strftime("%Y-%m-%d")
    for customer in customers[CUSTOMERS_COUNT:]:
        new_signups.append(
            [
                customer[0],  # SIGNUP ID
                customer[0],  # CUSTOMER ID
                f"abcd@example.com",  # USER EMAIL
                hashlib.sha256(datetime.now().isoformat().encode()).hexdigest(),
                validation_signup_date,
            ]
        )
    write_to_csv(signups_anomalies_data_path, signups_headers, new_signups)
