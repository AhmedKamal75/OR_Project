import random
import simpy
import numpy as np
import matplotlib.pyplot as plt


NUM_OF_EMPLOYEES = 2
AVG_SERVICE_RATE = 5
ARRIVAL_RATE = 2
SIM_TIME = 120

CUSTOMERS_HANDLED = 0

class CallCenter():
    def __init__(self, env, num_of_empolyees, avg_service_rate, arrival_rate):
        self.env = env
        self.staff = simpy.Resource(env, num_of_empolyees)
        self.avg_service_rate = avg_service_rate
        self.arrival_rate = arrival_rate
        self.customer_entered_service = 0
        
    

    def serve_customer(self, customer):
        self.customer_entered_service += 1
        random_service_time = (np.random.exponential(1.0/self.avg_service_rate))
        yield self.env.timeout(random_service_time)
        print(f"Customer {customer} served at {self.env.now}, took {random_service_time} time units.")
        
    def cutomer_arrival(self):
        while True:
            random_arrival_time = (np.random.exponential(1.0/self.arrival_rate))
            yield self.env.timeout(random_arrival_time)
            self.customer_entered_service += 1
            print(f"Customer {self.customer_entered_service} arrived at {self.env.now}")
            self.env.process(customer(self.env, id, self))

def customer(env, id, call_center):
    global CUSTOMERS_HANDLED
    arrival_time = env.now
    print(f"Customer {str(id)} arrived at {arrival_time}")
    with call_center.staff.request() as request:
        yield request
        print(f"Customer {str(id)} enter service at {env.now}")
        yield env.process(call_center.serve_customer(id))
        print(f"Customer {str(id)} leave service at {env.now}")
        CUSTOMERS_HANDLED += 1


def setup(env, num_of_employees, avg_service_rate, arrival_rate, customers_already_in_queue):
    call_center = CallCenter(env, num_of_employees, avg_service_rate, arrival_rate)
    
    for i in range(customers_already_in_queue):
        env.process(customer(env, i, call_center))
        
    env.process(call_center.cutomer_arrival())
    

if __name__ == "__main__":
    env = simpy.Environment()
    setup(env, NUM_OF_EMPLOYEES, AVG_SERVICE_RATE, ARRIVAL_RATE, 10)
    env.run(until=SIM_TIME)

    print(f"Customers handled: {CUSTOMERS_HANDLED}")
    print(f"time elapsed: {env.now}")
    
    

    