#!/usr/bin/env python3
"""
    api authentication
"""
from flask import request


class Auth:
    """ a class that manage api authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        if path not in excluded_paths:
            return True

        elif if path is None:
            return True

        elif excluded_paths is None or len(excluded_paths) == 0:
            return True

        elif if path is in excluded_paths:
            return False

        for excluded_path in exclude_paths:
            if path.startswith(excluded_path.rstrip('/') + '/'):
                return False

        return False

    def authorization_header(self, request=None) -> str:
        if request is None:
            return None

        if 'Authorization' not in request.headers:
            return None
        else:
            return request.headers['Authorization']

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        return None
