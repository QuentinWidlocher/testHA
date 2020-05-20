def function(param, callback):
    print(f"function : {param}")
    callback(param)

def callback(param, wow = "wow"):
    print(f"callback : {param}, {wow}")

function("prout", callback)
