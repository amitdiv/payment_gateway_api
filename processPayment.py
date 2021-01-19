import datetime
import configparser
import logging
from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse
app = Flask(__name__)
api = Api(app)


class Pay(Resource):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s :: %(levelname)s :: %(lineno)d :: %(message)s',filename='call_execution.log')

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.config = configparser.ConfigParser()
        self.config.read("mocked_payment_confirmation.conf")
        self.reqparse.add_argument('number', type=str, default=0, required=True)
        self.reqparse.add_argument('owner', type=str, default='', required=True)
        self.reqparse.add_argument('expiry', type=str, default='1', required=True)
        self.reqparse.add_argument('secure_code', type=str, default='')
        self.reqparse.add_argument('amount', type=float, default=0, required=True)
        self.curr_time=str(datetime.datetime.today().strftime('%Y-%m-%d'))

    def get(self):
        logging.info("Invoking GET request to api")
        try:
            ret_val = 0
            config = None
            args = self.reqparse.parse_args()
            args['expiry'] = str(datetime.datetime.strptime(args['expiry'], "%Y-%m-%d").date())
            if len(args['number'])!=16 or args['expiry']<self.curr_time or not args['owner'] or (not args['amount'] or args['amount']<1):
                logging.error("One of the parameters in api call has not fulfilled the requirement. Exiting execution")
                return self.return_400()
            elif not args['secure_code'] or len(args['secure_code'])!=3:
                logging.warning("Either secure_code provided is null or incorrect. Please check")
                return "Please provide a valid secure_code to process the payment"
            elif args['amount']<20:
                logging.info("Payment is getting processed through cheappaymentgateway")
                ret_val,config=self.cheappaymentgateway(args['amount'],args['owner'])
            elif args['amount']>20 and args['amount']<501:
                logging.info("Payment is getting processed through expensivepaymentgateway")
                ret_val,config=self.expensivepaymentgateway(args['amount'],args['owner'])
                if ret_val!=1:
                    logging.info("Payment is getting processed through cheappaymentgateway because expensivepaymentgateway is not responding")
                    ret_val,config = self.cheappaymentgateway(args['amount'],args['owner'])
            elif args['amount']>500:
                for i in range(3):
                    logging.info("Payment is getting processed through premiumpaymentgateway")
                    ret_val,config=self.premiumpaymentgateway(args['amount'],args['owner'])
                    if ret_val==1:
                        break
            else:
                logging.error("The request made was invalid hence api failed to respond. Exiting execution")
                return self.return_500()
            with open("mocked_payment_confirmation.conf","w") as file:
                config.write(file)
            if ret_val==1:
                logging.info("Processing of payment completed successfully.")
                return self.return_200()
            else:
                logging.error("Processing of payment failed")
                return self.return_400()
        except Exception as e:
            return "An Exception occurred : {0}".format(e)

    def return_500(self):
        return "500 internal server error"

    def return_400(self):
        return "400 bad request: The request is invalid"

    def return_200(self):
        return "Payment is processed: 200 OK"

    def cheappaymentgateway(self,*args):
        try:
            self.config.set("Euros_20","amount_submitted",str(args[0]))
            self.config.set("Euros_20", "submitter_name", str(args[1]))
            return 1,self.config
        except Exception as e:
            return 0,None

    def expensivepaymentgateway(self,*args):
        try:
            self.config.set("Euros_500","amount_submitted",str(args[0]))
            self.config.set("Euros_500", "submitter_name", str(args[1]))
            return 1,self.config
        except Exception as e:
            return 0,None

    def premiumpaymentgateway(self,*args):
        try:
            self.config.set("Euros_501","amount_submitted",str(args[0]))
            self.config.set("Euros_501", "submitter_name", str(args[1]))
            return 1,self.config
        except Exception as e:
            return 0,None

api.add_resource(Pay, '/payment_gateway')


if __name__ == '__main__':
    app.run(debug=True)

