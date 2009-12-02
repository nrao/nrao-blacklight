# You can configure Blacklight from here.
#
#   Blacklight.configure(:environment) do |config| end
#
# :shared (or leave it blank) is used by all environments.
# You can override a shared key by using that key in a particular
# environment's configuration.
#
# If you have no configuration beyond :shared for an environment, you
# do not need to call configure() for that envirnoment.
#
# For specific environments:
#
#   Blacklight.configure(:test) {}
#   Blacklight.configure(:development) {}
#   Blacklight.configure(:production) {}
#

Blacklight.configure(:shared) do |config|

  # default params for the SolrDocument.search method
  SolrDocument.default_params[:search] = {
    :qt=>:search,
    :per_page => 10,
    :facets => {:fields=>
      [      "decade_facet",
             "year",
             "instrument_facet",
             "survey_facet",
             "availability",
             "ads_bibcode_status"
      ]
    }
  }

  # default params for the SolrDocument.find_by_id method
  SolrDocument.default_params[:find_by_id] = {:qt => :document}

  ##############################

  config[:default_qt] = "search"

  # solr field values given special treatment in the show (single result) view
  config[:show] = {
    :html_title => "title_display",
    :heading => "title_display",
    :display_type => "format_code"
  }

  # solr fld values given special treatment in the index (search results) view
  config[:index] = {
    :show_link => "title_display",
    :num_per_page => 10,
    :record_display_type => "format_code"
  }

  # solr fields that will be treated as facets by the blacklight application
  #   The ordering of the field names is the order of the display
  config[:facet] = {
    :field_names => [
      "decade_facet",
      "year",
      "instrument_facet",
      "survey_facet",
      "availability",
      "ads_bibcode_status"
    ],
    :labels => {
      "decade_facet"            => "Decade",
      "year"                    => "Year",
      "instrument_facet"        => "Instrument",
      "survey_facet"            => "Survey",
      "availability"            => "Availability",
      "ads_bibcode_status"      => "ADS Bibcode"
    }
  }

  # solr fields to be displayed in the index (search results) view
  #   The ordering of the field names is the order of the display
  config[:index_fields] = {
    :field_names => [
      "institution",
      "year",
      "electronic_location"
    ],
    :labels => {
      "institution"             => "Institution:",
      "year"                    => "Year:",
      "electronic_location"     => "Online:",
    }
  }

  # solr fields to be displayed in the show (single result) view
  #   The ordering of the field names is the order of the display
  config[:show_fields] = {
    :field_names => [
      "title",
      "author",
      "institution",
      "year",
      "instruments_display",
      "surveys_display",
      "electronic_location",
      "availability_display",
      "ads_bibcode",
      "notes",
      "predoc"
    ],
    :labels => {
      "title"                   => "Title:",
      "author"                  => "Author:",
      "institution"             => "Institution:",
      "year"                    => "Year:",
      "instruments_display"     => "Instrument(s):",
      "surveys_display"         => "Survey(s):",
      "electronic_location"     => "Electronic Location:",
      "availability_display"    => "Availability:",
      "ads_bibcode"             => "ADS Bibcode:",
      "notes"                   => "Notes:",
      "predoc"                  => "Degree:"
    }
  }

  # type of raw data in index.  Currently marcxml and marc21 are supported.
  # config[:raw_storage_type] = "marcxml"
  # name of solr field containing raw data
  # config[:raw_storage_field] = "marc_display"

  # "fielded" search select (pulldown)
  # label in pulldown is followed by the name of a SOLR request handler as
  # defined in solr/conf/solrconfig.xml
  config[:search_fields] ||= []
  config[:search_fields] << ['All Fields', 'search']
  # config[:search_fields] << ['Author', 'author_search']
  # config[:search_fields] << ['Title', 'title_search']

  # "sort results by" select (pulldown)
  # label in pulldown is followed by the name of the SOLR field to sort by and
  # whether the sort is ascending or descending (it must be asc or desc
  # except in the relevancy case).
  # label is key, solr field is value
  config[:sort_fields] ||= []
  config[:sort_fields] << ['Relevance', '']
  config[:sort_fields] << ['Author, ascending', 'author_sort asc']
  config[:sort_fields] << ['Author, descending', 'author_sort desc']
  config[:sort_fields] << ['Title, ascending', 'title_sort asc']
  config[:sort_fields] << ['Title, descending', 'title_sort desc']
  config[:sort_fields] << ['Year, ascending', 'year_sort asc']
  config[:sort_fields] << ['Year, descending', 'year_sort desc']

  # the maximum number of search results to allow display of a spelling
  #  ("did you mean") suggestion, if one is available.
  config[:spell_max] = 2
end

