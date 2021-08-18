import numpy as np
import pandas as pd
from sklearn.gaussian_process import kernels
from continuum_gaussian_bandits import ContinuumArmedBandit, GPR

class ContextualContinuumArmedBandit:
    def __init__(self, contexts, oracle, bid_max_value, convergence_rate=1.0):
        self.context_dict = {}
        self.contexts = contexts
        self.bid_max_value = bid_max_value
        X = np.arange(0, self.bid_max_value, 100)
        self.num_contexts = len(contexts)
        for context in self.contexts:
            df_context = context.merge(X, how = 'right')
            y_pred = oracle.predict(df_context)
            self.context_dict[context] = (ContinuumArmedBandit(X, y_pred , convergence_rate=1.0), None, None)


    def select_action(self, context):
        continuum_bandit = self.contexts[context][0]
        x = continuum_bandit.select_action()
        return x
        
    def get_x_best(self, X, context):
        x_best = self.contexts[context][0].get_x_best(X)
        return x_best



    
    
    def fit(self, num_rounds):
        np.random.seed(42)
        for round_num in num_rounds:
            sample_context_id = np.random.randint(self.num_contexts)
            sampled_context = self.contexts[sample_context_id]
            continuum_bandit = self.context_dict[sampled_context][0]
            x = continuum_bandit.select_action()
            
            y_pred = self.oracle.predict(sampled_context.append(x))
            continuum_bandit.update(x, y_pred)
            
    
    def predict(self, contexts):
        result_set = []
        for context in contexts:
            try:
                sampled_context = self.context_dict[context]
            except:
                print("Unsampled or unseen context, please update or re-fit the model with the context included.")
                return Exception()
            result_set.append(self.get_x_best(np.arange(0, self.bid_max_value, 100), context))
            
        return np.array(result_set)
    
    def partial_fit(self, contexts_new, X_new, y_new, reward_new):
        for context in contexts_new:
            try:
                sampled_context = self.context_dict[context]
            except:
                print("Unsampled or unseen context, please update or re-fit the model with the context included.")
                return Exception()
            
            
            
            
            

