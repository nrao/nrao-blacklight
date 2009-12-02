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

  # FIXME: is this duplicated below?
  SolrDocument.marc_source_field  = :marc_display
  SolrDocument.marc_format_type   = :marc21
  SolrDocument.ead_source_field   = :xml_display

  # default params for the SolrDocument.search method
  SolrDocument.default_params[:search] = {
    :qt=>:search,
    :per_page => 10,
    :facets => {:fields=>
      [      "year",
             "session",
      ]
    }
  }

  # default params for the SolrDocument.find_by_id method
  SolrDocument.default_params[:find_by_id] = {:qt => :document}


  ##############################


  config[:default_qt] = "search"


  # solr field values given special treatment in the show (single result) view
  config[:show] = {
    :html_title => "title",
    :heading => "title",
    :display_type => "format_code"
  }

  # solr fld values given special treatment in the index (search results) view
  config[:index] = {
    :show_link => "title",
    :num_per_page => 10,
    :record_display_type => "format_code"
  }

  # solr fields that will be treated as facets by the blacklight application
  #   The ordering of the field names is the order of the display
  config[:facet] = {
    :field_names => [
      "year",
      "category",
      "firstauthor_facet",
      # "session",
    ],
    :labels => {
      "year"                    => "Year",
      "category"                => "Category",
      "firstauthor_facet"       => "First Author",
      "session"                 => "Session",
    }
  }

  # solr fields to be displayed in the index (search results) view
  #   The ordering of the field names is the order of the display
  config[:index_fields] = {
    :field_names => [
      "authors",
      "category_display",
      "year",
      "session"
    ],
    :labels => {
      "authors"                 => "Authors:",
      "category_display"        => "Category:",
      "year"                    => "Year:",
      "session"                 => "Session:"
    }
  }

  # solr fields to be displayed in the show (single result) view
  #   The ordering of the field names is the order of the display
  config[:show_fields] = {
    :field_names => [
      "authors",
      "abstract",
      "category_display",
      "year",
      "session",
      "filename",
      "pagenumbers",
    ],
    :labels => {
      "authors"                 => "Authors:",
      "abstract"                => "Abstract:",
      "category_display"        => "Category:",
      "year"                    => "Year:",
      "session"                 => "Session:",
      "filename"                => "Full-text:",
      "pagenumbers"             => "Page Number(s):",
    }
  }

  # FIXME: is this now redundant with above?
  # type of raw data in index.  Currently marcxml and marc21 are supported.
  # config[:raw_storage_type] = "marc21"
  # name of solr field containing raw data
  # config[:raw_storage_field] = "marc_display"

  # "fielded" search select (pulldown)
  # label in pulldown is followed by the name of a SOLR request handler as
  # defined in solr/conf/solrconfig.xml
  config[:search_fields] ||= []
  config[:search_fields] << ['All Fields', 'search']
  # config[:search_fields] << ['Author', 'author_search']
  # config[:search_fields] << ['First Author', 'first_author_search']
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
  config[:sort_fields] << ['Record Modified, ascending', 'modified_sort asc']
  config[:sort_fields] << ['Record Modified, descending', 'modified_sort desc']
  config[:sort_fields] << ['Record Created, ascending', 'created_sort asc']
  config[:sort_fields] << ['Record Created, descending', 'created_sort desc']

  # If there are more than this many search results, no spelling ("did you
  # mean") suggestion is offered.
  config[:spell_max] = 2
end

