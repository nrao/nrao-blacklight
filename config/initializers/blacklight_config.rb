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
    :facets => {
      :fields => [
        "telescope",
        "year",
        "band_facet",
        "receiver_facet",
        "detector_facet",
      ]
    }
  }

  # default params for the SolrDocument.find_by_id method
  SolrDocument.default_params[:find_by_id] = {:qt => :document}

  ##############################

  config[:default_qt] = "search"

  # solr field values given special treatment in the show (single result) view
  config[:show] = {
    :html_title => "id",
    :heading => "id",
    :display_type => "format_code"
  }

  # solr fld values given special treatment in the index (search results) view
  config[:index] = {
    :show_link => "id",
    :num_per_page => 10,
    :record_display_type => "format_code"
  }

  # solr fields that will be treated as facets by the blacklight application
  #   The ordering of the field names is the order of the display
  config[:facet] = {
    :field_names => [
      "telescope",
      "year",
      "band_facet",
      "receiver_facet",
      "detector_facet",
    ],
    :labels => {
      "telescope"               => "Telescope",
      "year"                    => "Year",
      "band_facet"              => "Band",
      "receiver_facet"          => "Receiver",
      "detector_facet"          => "Detector",
    }
  }

  # solr fields to be displayed in the index (search results) view
  #   The ordering of the field names is the order of the display
  config[:index_fields] = {
    :field_names => [
      "telescope",
      # "investigator_display", # include marker of who is PI
      "source_display",
      "frequency_display",
    ],
    :labels => {
      "telescope"               => "Telescope:",
      "investigator_display"    => "Investigators:",
      "source_display"          => "Source:",
      "frequency_display"       => "Frequency (GHz):",
    }
  }

  # solr fields to be displayed in the show (single result) view
  #   The ordering of the field names is the order of the display
  config[:show_fields] = {
    :field_names => [
      "telescope",
      # "title",
      # "investigator_display",
      # "abstract",
      "source_display",
      "frequency_display",
      "lastdate",
      "receiver_display",
      "detector_display",
      # "bandwidth_display",
      "polarization_display",
    ],
    :labels => {
      "telescope"               => "Telescope:",
      "title"                   => "Title:",
      "investigator_display"    => "Investigators:",
      "abstract"                => "Abstract:",
      "source_display"          => "Source:",
      "frequency_display"       => "Frequency (GHz):",
      "lastdate"                => "Last Observation:",
      "band_display"            => "Band:",
      "receiver_display"        => "Receiver:",
      "detector_display"        => "Detector:",
      "bandwidth_display"       => "Bandwidth (MHz):",
      "polarization_display"    => "Polarization:",
    }
  }

  # "fielded" search select (pulldown)
  # label in pulldown is followed by the name of a SOLR request handler as
  # defined in solr/conf/solrconfig.xml
  config[:search_fields] ||= []
  config[:search_fields] << ['All Fields', 'search']
  # config[:search_fields] << ['Title', 'title_search']

  # "sort results by" select (pulldown)
  # label in pulldown is followed by the name of the SOLR field to sort by and
  # whether the sort is ascending or descending (it must be asc or desc
  # except in the relevancy case).
  # label is key, solr field is value
  config[:sort_fields] ||= []
  config[:sort_fields] << ['relevance', 'score desc, title_sort asc']

  # If there are more than this many search results, no spelling ("did you
  # mean") suggestion is offered.
  config[:spell_max] = 5
end

