# -*- coding: utf-8 -*-
'''
Copyright (c) 2015 Heidelberg University Library
Distributed under the GNU GPL v3. For full terms see the file
LICENSE.md
'''
from gluon.storage import Storage
from gluon.custom_import import track_changes
settings = Storage()

settings.migrate = True
settings.title = 'Heidelberg Asian Studies Publishing - HASP'
settings.short_title = 'HASP'
settings.subtitle = ''
settings.author_email = 'heiup@ub.uni-heidelberg.de'
settings.keywords = ''
settings.description = 'Heidelberg Asian Studies Publishing (HASP) ist die Open-Access Publikationsplattform des FID4SA-Fachinformationsdienst Südasien. HASP veröffentlicht wissenschaftliche e-Books aus dem Bereich der Asienwissenschaften.'
settings.layout_theme = 'Default'
# settings.database_uri = 'sqlite://storage.sqlite'
# settings.database_uri = 'mysql://omp-user:omp-password@localhost:3306/omptest'
settings.security_key = '1228409b-a1fc-4868-92b1-a973a607d3f1'
settings.email_server = 'login'
settings.email_sender = 'login'
settings.email_login = ''
settings.login_method = 'local'
settings.login_config = ''
settings.plugins = []

track_changes(True)
