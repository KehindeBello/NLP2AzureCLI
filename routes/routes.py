from flask_restful import Api
from resources import UserLogin, UserRegister, UserLogout, ResetPassword, ConvertNLP, ForgotPassword, RunCommandInCli, Callback
def create_routes(app):
    api = Api(app)

    api.add_resource(UserLogin, "/login", endpoint="login")
    api.add_resource(UserRegister, "/signup", endpoint="signup")
    api.add_resource(UserLogout, "/logout")
    api.add_resource(ForgotPassword, "/forgot_password", endpoint="forgot_password")
    api.add_resource(ResetPassword, "/reset_password/<token>")
    api.add_resource(ConvertNLP, '/convert')
    api.add_resource(RunCommandInCli, '/run')

    return api