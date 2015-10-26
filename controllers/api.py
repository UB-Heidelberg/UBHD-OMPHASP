# -*- coding: utf-8 -*-
'''
Copyright (c) 2015 Heidelberg University Library
Distributed under the GNU GPL v3. For full terms see the file
LICENSE.md
'''
import gluon.contrib.simplejson as sj
def oastatistik():
  locale = 'de_DE'
  if session.forced_language == 'en':
    locale = 'en_US'
  query = ((db.submissions.context_id == myconf.take('omp.press_id')) & (db.submissions.status == 3) & (
        db.submission_settings.submission_id == db.submissions.submission_id) & (db.submission_settings.locale == locale))
  submissions = db(query).select(db.submission_settings.ALL,orderby=db.submissions.submission_id)
  subs = {}
  title, publication_format_settings_doi  ='',None
  
 
  for book_id in submissions:  
    
    if request.vars.fullbooks=='true' or request.vars.chapters == None:
    # full book 
      publication_format_settings = db((db.publication_format_settings.setting_name == 'name') & (db.publication_format_settings.locale == locale) & (db.publication_formats.submission_id == book_id['submission_id']) & (db.publication_formats.publication_format_id == db.publication_format_settings.publication_format_id)).select(db.publication_format_settings.publication_format_id, db.publication_format_settings.setting_value)
      if publication_format_settings:
          publication_format_settings_doi = db((db.publication_format_settings.setting_name == 'pub-id::doi') & (db.publication_format_settings.publication_format_id == publication_format_settings.first()['publication_format_id'])\
          & (publication_format_settings.first()['setting_value'] == myconf.take('omp.doi_format_name'))).select(db.publication_format_settings.setting_value).first()

      if book_id.setting_name == 'title':
        title = book_id.setting_value
      authors = {}
      authors_list = db((db.authors.submission_id == book_id.submission_id)).select( db.authors.first_name, db.authors.last_name)
      for i in authors_list:
          authors['type'] = 'person'
          authors['relation'] = 'creators'
          authors['name'] = i.first_name + " "+ i.last_name
      fullbook = {}
      fullbook =  {}
      fullbook["label"] = title
      fullbook["type"] = "volume"
      if publication_format_settings_doi :
        fullbook["norm_id"] = publication_format_settings_doi['setting_value']
      fullbook["associate_via_hierarchy"] = authors
      subs[book_id.submission_id] = fullbook

    
    # chapters
    if request.vars.chapters=='true' or request.vars.fullbooks == None:
      chapters = db (db.submission_chapters.submission_id == book_id['submission_id']).select(db.submission_chapters.chapter_id, orderby = db.submission_chapters.chapter_seq)
      for c in chapters:
        chapter_id = str(book_id['submission_id'])+'-'+str(c['chapter_id'])
        subs[chapter_id]= {}
        part_title = db((db.submission_chapter_settings.chapter_id ==  int(c['chapter_id'])) & (db.submission_chapter_settings.locale == locale) & (db.submission_chapter_settings.setting_name == 'title')).select(db.submission_chapter_settings.setting_value).first()
        if part_title:
          subs[chapter_id]["label"] = part_title['setting_value']
        subs[chapter_id]["norm_id"] =  myconf.take('oastatistik.id')+':'+chapter_id
        subs[chapter_id]["type"] = "part"
        part_authors = []
        author_id_list = db(db.submission_chapter_authors.chapter_id ==int(c['chapter_id']) ).select (db.submission_chapter_authors.author_id, orderby = db.submission_chapter_authors.seq)
        for author in author_id_list :
          part_authors.append({"type":"person"})
          part_authors.append({"relation":"creators"})
          author_name = db((db.authors.author_id == author['author_id'])).select( db.authors.first_name, db.authors.last_name).first()
          if author_name:
            part_authors.append({'name': author_name['first_name'] + " "+ author_name['last_name']})


        subs[chapter_id]["associate_via_hierarchy"] = part_authors
    
          
    
 
  #full = ([[r.submissions.submission_id] for r in submissions])
  return sj.dumps(subs, separators=(',', ':'), sort_keys=True)