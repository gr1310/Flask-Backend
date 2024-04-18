from flask import Flask
from flask_restful import Api, Resource

app= Flask(__name__)
api= Api(app)

names={"Garima": {"age": 20, "gender":"Female"},"Tim":{"age":19, "gender":"Male"}}

class HelloWorld(Resource):
    def get(self,name):
        # return {"data":name,"test":test}
        return names[name]
    def post(self):
        return {"data":"Posted"}
    
# api.add_resource(HelloWorld,"/helloworld/<string:name>/<int:test>")
api.add_resource(HelloWorld,"/helloworld/<string:name>")

if __name__=="__main__":
    app.run(debug=True)