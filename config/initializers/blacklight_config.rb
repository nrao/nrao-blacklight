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
        "format",
      ]
    }
  }

  # default params for the SolrDocument.find_by_id method
  SolrDocument.default_params[:find_by_id] = {:qt => :document}

  ##############################

  config[:default_qt] = "search"

  # solr field values given special treatment in the show (single result) view
  config[:show] = {
    :html_title => "project",
    :heading => "project",
    :display_type => "format"
  }

  # solr fld values given special treatment in the index (search results) view
  config[:index] = {
    :show_link => "project",
    :num_per_page => 10,
    :record_display_type => "format"
  }

  # solr fields that will be treated as facets by the blacklight application
  #   The ordering of the field names is the order of the display
  config[:facet] = {
    :field_names => [
      "format",
    ],
    :labels => {
      "format"              => "Format",
    }
  }

  # solr fields to be displayed in the index (search results) view
  #   The ordering of the field names is the order of the display
  config[:index_fields] = {
    :field_names => [
      "source",
      "project",
      "frequency_mhz",
      "tele_conf_sub_nant",
      "lasttime",
    ],
    :labels => {
      "source" => "Source",
      "project" => "Project",
      "frequency_mhz" => "Frequency (MHz)",
      "distance_arcmin" => "Distance (arcmin)",
      "tos_sec" => "TOS (sec)",
      "rms_mjy" => "rms (mJy)",
      "resolution_arcsec" => "resolution (arcsec)",
      "fov_arcmin" => "FOV (arcmin)",
      "tele_conf_sub_nant" => "Tele:conf:sub:nant",
      "chans" => "Chans",
      "bw_mhz" => "BW (MHz)",
      "polar" => "Polar",
      "firsttime" => "FirstTime",
      "lasttime" => "LastTime",
      "ra" => "Ra (?)",
      "dec" => "Dec (?)",
    }
  }

  # solr fields to be displayed in the show (single result) view
  #   The ordering of the field names is the order of the display
  config[:show_fields] = {
    :field_names => [
      "source",
      "project",
      "frequency_mhz",
      "distance_arcmin",
      "tos_sec",
      "rms_mjy",
      "resolution_arcsec",
      "fov_arcmin",
      "tele_conf_sub_nant",
      "chans",
      "bw_mhz",
      "polar",
      "firsttime",
      "lasttime",
      "ra",
      "dec",
    ],
    :labels => {
      "source" => "Source",
      "project" => "Project",
      "frequency_mhz" => "Frequency (MHz)",
      "distance_arcmin" => "Distance (arcmin)",
      "tos_sec" => "TOS (sec)",
      "rms_mjy" => "rms (mJy)",
      "resolution_arcsec" => "resolution (arcsec)",
      "fov_arcmin" => "FOV (arcmin)",
      "tele_conf_sub_nant" => "Tele:conf:sub:nant",
      "chans" => "Chans",
      "bw_mhz" => "BW (MHz)",
      "polar" => "Polar",
      "firsttime" => "FirstTime",
      "lasttime" => "LastTime",
      "ra" => "Ra (?)",
      "dec" => "Dec (?)",
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

