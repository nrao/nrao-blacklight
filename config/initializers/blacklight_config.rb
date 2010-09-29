# NOTICE: See app/views/catalog/_document_list.html.erb - bypasses this config!
# Facets are still configured via this document.
#
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
        "configuration_facet" => "EVLA/VLA Array Config.",
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
        "project" => "Project",
        "telescope_display" => "Telescope",
        "obs_bands" => "Band",
        "proprietary" => "Proprietary",
        "format" => "Format",
        "filesize_display" => "Filesize (MB)",
        "starttime" => "Data Starts",
        "stoptime" => "Data Stops",
        "type" => "Type",
        "band" => "Band",
        "band_facet" => "Band",
    }

  # solr fields that will be treated as facets by the blacklight application
  #   The ordering of the field names is the order of the display
  config[:facet] = {
    :field_names => [
        "telescope_facet",
        "proprietary",
        "band_facet",
        "configuration_facet",
    ],
    :labels => labels
  }

# NOTICE: See app/views/catalog/_document_list.html.erb - bypasses this config!
# NOTICE: See app/views/catalog/_document_list.html.erb - bypasses this config!

  # solr fields to be displayed in the index (search results) view
  #   The ordering of the field names is the order of the display
  config[:index_fields] = {
    :field_names => [
        "project",
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
        "project",
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
  config[:sort_fields] << ['Relevance', 'score desc']
  config[:sort_fields] << ['Date, oldest first', 'starttime asc']
  config[:sort_fields] << ['Date, newest first', 'starttime desc']
  config[:sort_fields] << ['PI, ascending', 'investigator_sort asc']
  config[:sort_fields] << ['PI, descending', 'investigator_sort desc']

  # TODO: add these to sort
  #  date asc
  #  date desc
  #  pi asc (last name first)
  #  pi desc (last name first)

  # If there are more than this many search results, no spelling ("did you
  # mean") suggestion is offered.
  config[:spell_max] = 5
end

