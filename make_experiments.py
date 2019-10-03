from outfit import Wardrobe
import datetime


wardrobe = Wardrobe(db_path='./expe.db')

exp = {
    'experiment_name': 'VGG16',
    'comment': 'VGG16 exp',
    'date_experiment': datetime.datetime.now()
}

wardrobe.add_experiment(**exp)

param = {
    'dropout': 0.03,
    'lr': 0.001,
    'batch_size': 200 
}

wardrobe.add_dict_parameter(param)


score = {
    'train acc': 0.85,
    'train loss': 0.460,
    'val acc': 0.83,
    'val loss': 0.480
}

wardrobe.add_dict_score(score)
wardrobe.tidy()


