import random
import numpy as np
import simpy as sim
import matplotlib.pyplot as plt

QUEUE1_LENGTH = []
QUEUE2_LENGTH = []
QUEUE1_ALL_CUSTOMERS = 0
QUEUE2_ALL_CUSTOMERS = 0
QUEUE1_CUSTOMER_SERVED = 0
QUEUE2_CUSTOMER_SERVED = 0



class Queue1():
    def __init__(self, env,lambda_, mu, next_queue):
        self.env = env
        self.lambda_ = lambda_
        self.mu = mu
        self.next_queue = next_queue
        self.servers = sim.Resource(env, capacity=1)
        self.customers_entered_queue = 0
        self.customers_served = 0
        self.current_number_of_customers_in_queue = 0
        self.queue_length = [] # over time
        
    def arrival(self):
        while True:
            random_arrival_time = np.ceil(np.random.exponential(1.0/self.lambda_))
            yield self.env.timeout(random_arrival_time)
            self.customers_entered_queue += 1
            print(f"Customer {self.customers_entered_queue} entered the queue.")
            self.current_number_of_customers_in_queue += 1
            with self.servers.request() as request:
                yield request
                yield self.env.process(self.service())
        
    def service(self):
        random_service_time = np.ceil(np.random.exponential(1.0/self.mu))
        yield self.env.timeout(random_service_time)
        self.customers_served += 1
        self.current_number_of_customers_in_queue -= 1
        
        # handle entering the second queue
        self.env.process(self.next_queue.arrival())

    def monitor(self):
        while True:
            self.queue_length.append((env.now, self.current_number_of_customers_in_queue))
            yield self.env.timeout(1)
        
class Queue2():
    def __init__(self,env,mu):
        self.env = env
        self.mu = mu
        self.servers = sim.Resource(env, capacity=1)
        self.customers_entered_queue = 0
        self.customers_served = 0
        self.current_number_of_customers_in_queue = 0
        self.queue_length = [] # over time

    def arrival(self):
        self.customers_entered_queue += 1
        self.current_number_of_customers_in_queue += 1
        with self.servers.request() as request:
            yield request
            yield self.env.process(self.service())
            
    def service(self):
        random_service_time = np.ceil(np.random.exponential(1.0/self.mu))
        yield self.env.timeout(random_service_time)
        self.customers_served += 1
        self.current_number_of_customers_in_queue -= 1

    def monitor(self):
        while True:
            self.queue_length.append((env.now, self.current_number_of_customers_in_queue))
            yield self.env.timeout(1)

        
def setup(env, lambda_, mu1, mu2, q):
    queue2 = Queue2(env, mu2)
    queue1 = Queue1(env, lambda_, mu1, queue2)
    
    for i in range(q):
        with queue1.servers.request() as request:
            yield request
            yield env.process(queue1.service())
    
    env.process(queue1.arrival())
    env.process(queue1.monitor())
    env.process(queue2.monitor())
    
    global QUEUE1_ALL_CUSTOMERS
    global QUEUE2_ALL_CUSTOMERS
    
    QUEUE1_ALL_CUSTOMERS = queue1.customers_entered_queue
    QUEUE2_ALL_CUSTOMERS = queue2.customers_entered_queue
    
    global QUEUE1_CUSTOMER_SERVED
    global QUEUE2_CUSTOMER_SERVED
    
    QUEUE1_CUSTOMER_SERVED = queue1.customers_served
    QUEUE2_CUSTOMER_SERVED = queue2.customers_served
    
    global QUEUE1_LENGTH
    global QUEUE2_LENGTH
    
    QUEUE1_LENGTH = queue1.queue_length
    QUEUE2_LENGTH = queue2.queue_length
    
    # return (queue1, queue2)
    
    
if __name__ == "__main__":
    env = sim.Environment()
    lambda_ = 1
    mu1 = 2
    mu2 = 4
    q = 10
    T = 100
    
    setup(env, lambda_=lambda_, mu1=mu1, mu2=mu2, q=q)
    
    env.run(until=T)
    
        # Print the results for demonstration
    print(f"Queue 1: Entered: {QUEUE1_ALL_CUSTOMERS}, Served: {QUEUE1_CUSTOMER_SERVED}")
    print(f"Queue 2: Entered: {QUEUE2_ALL_CUSTOMERS}, Served: {QUEUE2_CUSTOMER_SERVED}")


    print(QUEUE1_LENGTH)
    print(QUEUE2_LENGTH)
    # Plotting the results
    # times1, lengths1 = zip(*queue1.queue_length_over_time) if queue1.queue_length_over_time else ([], [])
    # times2, lengths2 = zip(*queue2.queue_length_over_time) if queue2.queue_length_over_time else ([], [])

    # plt.figure(figsize=(12, 6))
    # plt.plot(times1, lengths1, label='Queue 1 Length Over Time')
    # plt.plot(times2, lengths2, label='Queue 2 Length Over Time')
    # plt.xlabel('Time')
    # plt.ylabel('Queue Length')
    # plt.title('Queue Lengths Over Time')
    # plt.legend()
    # plt.show()
