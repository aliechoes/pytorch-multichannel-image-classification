import pandas as pd 
from sklearn.metrics import  accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import log_loss
import numpy as np
from sklearn.metrics import confusion_matrix
import logging

def custom_log_loss(y_true, y_pred, existing_labels): 
    custom_y_pred = np.zeros((y_true.shape[0], len(existing_labels)))
    
    for i in range(0, len(y_true)):
        j = y_pred[i]
        custom_y_pred[i,j ] = 1  
    return log_loss(y_true, custom_y_pred, labels=existing_labels)


def metric_history(df, metric_dataframe, epoch, metrics_of_interest ):
 
    existing_labels = df["label"].unique().tolist()
    for s in ["train", "validation", "test"]:
        logging.info(10*"---") 
        
        df_temp = df[ df["set"]==s].reset_index(drop = True).copy()
        
        if df_temp.shape[0] > 0:
            y_true = df_temp["label"].astype(int)
            y_pred = df_temp["prediction"].astype(int)
            
            assert (y_pred == -1).sum()== 0  
            

            if "accuracy" in metrics_of_interest:
                results_temp = {
                    'epoch': epoch,
                    'set':   s,
                    'metric': 'accuracy',
                    'value': accuracy_score(y_true, y_pred ) 
                }
                logging.info("epoch %d: accuracy for the %s set is %f" % (epoch, s, accuracy_score(y_true, y_pred ) ) )
                metric_dataframe = metric_dataframe.append(results_temp, ignore_index=True)

            if "cross_entropy" in metrics_of_interest:
                    results_temp = {
                        'epoch': epoch,
                        'set':   s,
                        'metric': 'cross_entropy',
                        'value': custom_log_loss(y_true, y_pred, existing_labels) 
                    }
                    logging.info("cross_entropy for the %s set is: %f" % (s,  \
                        custom_log_loss(y_true, y_pred, existing_labels )  ) )
                    metric_dataframe = metric_dataframe.append(results_temp, ignore_index=True)
    
            
            if "f1_macro" in metrics_of_interest:
                results_temp = {
                    'epoch': epoch,
                    'set':   s,
                    'metric': 'f1_macro',
                    'value': f1_score(y_true, y_pred, average='macro' ) 
                }
                logging.info("f1_macro for the %s set is: %f" % (s, f1_score(y_true, y_pred, average='macro' ) ) )
                metric_dataframe = metric_dataframe.append(results_temp, ignore_index=True)
            
            
            if "f1_weighted" in metrics_of_interest:
                results_temp = {
                    'epoch': epoch,
                    'set':   s,
                    'metric': 'f1_weighted',
                    'value': f1_score(y_true, y_pred, average='weighted' ) 
                }
                logging.info("f1_weighted for the %s set is: %f" % (s, f1_score(y_true, y_pred, average='weighted' ) ) )
                metric_dataframe = metric_dataframe.append(results_temp, ignore_index=True)

        logging.info(10*"---")
    return metric_dataframe