from django.contrib.auth import get_user_model
from campaigns.models import AdvertiserUser
from django.http.response import HttpResponse, JsonResponse, HttpResponseServerError

class ApiAuthentication(object):
    keyword = 'ApiKey'

    def _authenticate(self, request, **kwargs):
        """
        Finds the user and validates their Apikey/Token.
        """

        """
        Try to extract the ``username`` and ``api_key`` from:
        1) ``Authorization`` header in the format ``ApiKey <username>:<api_key>``
        2) GET method url params ``username`` & ``api_key``
        3) POST method form keys ``username`` & ``api_key``
        """
        try:
            username, api_key = self.extract_credentials(request)
        except ValueError:
            return None

        if not username or not api_key:
            return None

        """
        get the default django user model
        """
        User = get_user_model()

        """
        takes multiple user models and try to get the user object
        from them respectively or returns ``False``
        """
        user = self.get_user(username, [AdvertiserUser, User])

        if not user:
            return False

        """
        validates the api_key/token
        """
        key_auth_check = self.validate_key(user, api_key)
        if key_auth_check:
            return (user, api_key,)

        return False

    def authenticate(self, request, **kwargs):
        """
        ### Rest framework compatible ###
        returns tuple of (user, token) if authenticated else
        returns None in case of no username, api_key/token were provided
        or raises rest_framework.exceptions.AuthenticationFailed error
        in case of invalid credentials
        """
        from rest_framework.exceptions import AuthenticationFailed
        auth = self._authenticate(request, **kwargs)
        if auth == False:
            raise AuthenticationFailed()

        return auth

    def is_authenticated(self, request, **kwargs):
        """
        ### Tastypie framework compatible ###
        returns either ``True`` if authenticated, ``False`` if not
        and updated the reuqest.user to the matching user in case of ``True``
        """
        authentication = self._authenticate(request, **kwargs)
        if authentication:
            request.user = authentication[0]
            request.auth = authentication[1]
            return True

        return False

    def extract_credentials(self, request):
        try:
            data = self.get_authorization_data(request)
        except ValueError:
            username = request.GET.get('username') or request.POST.get('username')
            api_key = request.GET.get('api_key') or request.POST.get('api_key')
        else:
            username, api_key = data.split(':', 1)

        return username, api_key

    def get_authorization_data(self, request):
        """
        Verifies that the HTTP Authorization header has the right auth type
        and returns the auth data.

        Raises ValueError when data could not be extracted.
        """
        authorization = request.META.get('HTTP_AUTHORIZATION', '')

        if not authorization:
            raise ValueError('Authorization header missing or empty.')

        try:
            auth_type, data = authorization.split(' ', 1)
        except:
            raise ValueError('Authorization header must have a space separating auth_type and data.')

        if auth_type.lower() != 'apikey':
            raise ValueError('auth_type is not "%s".' % 'ApiKey')

        return data

    def get_user(self, username, UserModelRefs):
        lookup_kwargs = {'username': username}

        for ModelRef in UserModelRefs:
            try:
                user = ModelRef.objects.select_related('api_key').get(**lookup_kwargs)
            except ModelRef.DoesNotExist:
                continue
            except ModelRef.MultipleObjectsReturned:
                return False
            else:
                return user if user.is_active else False

        return False

    def validate_key(self, user, api_key):
        """
        Attempts to find the API key / Token for the user and validate against it.
        """
        if hasattr(user, 'check_token'):
            return user.check_token(api_key)
        else:
            try:
                if user.api_key.key != api_key:
                    return False
            except user.api_key.RelatedObjectDoesNotExist:
                return False
            except Exception:
                return False
            else:
                return True

    def get_identifier(self, request):
        """
        Provides a unique string identifier for the requestor.
        """
        try:
            username = self.extract_credentials(request)[0]
        except ValueError:
            username = ''
        return username or 'nouser'

    def get_user_auth(self, user):
        try:
            if hasattr(user, 'get_token'):
                advertiser = user
            else:
                advertiser = AdvertiserUser.objects.get(id=user.id)
            token_exp = advertiser.get_token()
            username = advertiser.username
            token = token_exp[0]
            exp_ts = token_exp[1]
        except (AdvertiserUser.DoesNotExist):
            username = user.username
            token = user.api_key.key
            exp_ts = None

        auth = {
            'username': username,
            'api_key': token,
            'expiration': exp_ts
        }

        return auth

    def set_auth_cookie(self, user, response):
        auth = self.get_user_auth(user)
        response.set_cookie('ApiKey', '%s:%s' %(auth['username'], auth['api_key']), expires=auth['expiration'])
        response.set_cookie('username', user.username)
        return response

    def get_response_with_token(self, user):
        content = self.get_user_auth(user)
        return JsonResponse(content)

    def set_auth_headers(self, user, response):
        auth = self.get_user_auth(user)
        response['ApiKey'] = auth['api_key']
        response['Key-Expiration'] = auth['expiration']

    def authenticate_header(self, request):
        return self.keyword

api_auth = ApiAuthentication()


def authenticate_view(view_func):
    """
    A decorator function that authenticates django views
    """
    def _wrapped_view_func(request, *args, **kwargs):
        if not api_auth.is_authenticated(request):
            return HttpResponse('Unauthorized', status=401)
        else:
            return view_func(request, *args, **kwargs)
    return _wrapped_view_func
