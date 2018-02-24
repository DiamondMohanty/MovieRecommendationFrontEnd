# project/server/config.py

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    """Base configuration."""
    SECRET_KEY = 'my_precious'
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'mysql://root:rabindra_bls@localhost/OishiiDev'
    DEBUG_TB_ENABLED = True
    MAIL_CREDENTIALS="kk.sagar@oishii.co.in:S@112358"
    # account_sid:auth_token
    SMS_CREDENTIALS="AC68485ad7747ab52c1ef3603f52709394:23af59ada6875ca6b334325a6825c638"


class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'
    DEBUG_TB_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(BaseConfig):
    """Production configuration."""
    SECRET_KEY = '14qn8s0plxg)k!!f!b=p%rc9t2xca^(5mu+aaly86blqa2rfkr'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}'.format(
    username="Devmob",
    password="Lotus@2018",
    hostname="Devmob.mysql.pythonanywhere-services.com",
    databasename="Devmob$OishiiDev",
    )
    DEBUG_TB_ENABLED = False
    MAIL_CREDENTIALS="kk.sagar@oishii.co.in:S@112358"
    SMS_CREDENTIALS="AC68485ad7747ab52c1ef3603f52709394:23af59ada6875ca6b334325a6825c638"
