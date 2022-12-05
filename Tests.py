import pickle as pk
import Pendule_class as pc


pendule = pc.Pendulum(0,0,range(0,10),1,1,1,1,1,1,1,"test_log.csv")
with open("pickl", "wb") as f:
    pk.dump(pendule, f)
