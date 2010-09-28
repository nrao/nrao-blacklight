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
  }

  # default params for the SolrDocument.find_by_id method
  SolrDocument.default_params[:find_by_id] = {:qt => :document}

  ##############################

  config[:default_qt] = "search"

  # solr field values given special treatment in the show (single result) view
  config[:show] = {
    :html_title => "id_display",
    :heading => "id_display",
    :display_type => "format_code"
  }

  # solr fld values given special treatment in the index (search results) view
  config[:index] = {
    :show_link => "id_display",
    :num_per_page => 10,
    :record_display_type => "format_code"
  }

  labels = {
        "source" => "Source",
        "project" => "Project",
        "proprietary" => "Proprietary",
        "frequency" => "Frequency (MHz)",
        "frequency_display" => "Frequency (MHz)",
        "distance" => "Distance (arcmin)",
        "tos" => "TOS (sec)",
        "rms" => "rms (mJy)",
        "resolution" => "Resolution (arcsec)",
        "fov" => "FOV (arcmin)",
        "tele_conf_sub_nant" => "Tel:conf:sub:nant",
        "telescope" => "Telescope",
        "telescope_facet" => "Telescope",
        "configuration" => "Conf",
        "configuration_facet" => "Conf",
        "sub" => "Sub",
        "nant" => "# Ant.",
        "chans" => "Channels",
        "bw" => "Bandwidth (MHz)",
        "polar" => "Polar",
        "polar_facet" => "Polar",
        "start" => "First",
        "stop" => "Last",
        "ra" => "RA (J2000 rad)",
        "dec" => "Dec (J2000 rad)",
        "arch_file_id" => "File ID",
        "project_code" => "Project",
        "telescope_display" => "Telescope",
        "obs_bands" => "Band",
        "proprietary" => "Proprietary",
        "format" => "Format",
        "filesize_display" => "Filesize (MB)",
        "starttime" => "Data Starts",
        "stoptime" => "Data Stops",
        "type" => "Type",
    }

  # solr fields that will be treated as facets by the blacklight application
  #   The ordering of the field names is the order of the display
  config[:facet] = {
    :field_names => [
        "telescope_facet",
        "band_facet",
        "proprietary",
        "type",
        "format",
    ],
    :labels => labels
  }

  # solr fields to be displayed in the index (search results) view
  #   The ordering of the field names is the order of the display
  config[:index_fields] = {
    :field_names => [
        "project_code",
        "telescope_display",
        "obs_bands",
        "proprietary",
        "format",
        "type",
        "filesize_display",
        "starttime",
        "stoptime",
    ],
    :labels => labels
  }

  # solr fields to be displayed in the show (single result) view
  #   The ordering of the field names is the order of the display
  config[:show_fields] = {
    :field_names => [
        "project_code",
        "telescope_display",
        "obs_bands",
        "proprietary",
        "format",
        "type",
        "filesize_display",
        "starttime",
        "stoptime",

        "source",
        "frequency",
        "tele_conf_sub_nants",
        "chans",
        "polar",
        "first",
        "last",
        "ra",
        "dec",
    ],
    :labels => labels
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
  config[:sort_fields] << ['relevance', 'score desc']

  # If there are more than this many search results, no spelling ("did you
  # mean") suggestion is offered.
  config[:spell_max] = 5
end

