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
      "band_facet",
      "receiver_facet",
      "backend_facet",
      "obstype_facet",
      "procname_facet",
    ],
    :labels => {
      "band_facet" => "Band",
      "receiver_facet" => "Receiver",
      "backend_facet" => "Backend",
      "obstype_facet" => "Observing Type",
      "procname_facet" => "Procedure Name",
    }
  }

  # solr fields to be displayed in the index (search results) view
  #   The ordering of the field names is the order of the display
  config[:index_fields] = {
    :field_names => [
      "telescope",
      "title",
      "investigator_display",
      "object",
      "band",
      "receiver",
      "backend",
      "obstype",
      "ra",
      "dec",
      "skyfreq",
    ],
    :labels => {
      "telescope" => "Telescope",
      "proposal_id" => "Proposal ID",
      "legacy_id" => "Legacy ID",
      "title" => "Title",
      "abstract" => "Abstract",
      "investigator_display" => "Investigators",
      "object" => "Object",
      "observer" => "Observer",
      "date-obs" => "Date Observed",
      "velocity" => "Velocity",
      "veldef" => "Velocity Definition",
      "skyfreq" => "Sky Frequency (GHz)",
      "restfreq" => "Rest Frequency (GHz)",
      "ra" => "RA (J2000)",
      "dec" => "Dec (J2000)",
      "pol" => "Polarization",
      "bandwidth" => "Bandwidth (MHz)",
      "band" => "Band",
      "receiver" => "Receiver",
      "backend" => "Backend",
      "obstype" => "Observing Type",
      "procname" => "Procedure Name",
    }
  }

  # solr fields to be displayed in the show (single result) view
  #   The ordering of the field names is the order of the display
  config[:show_fields] = {
    :field_names => [
      "telescope",
      "proposal_id",
      "legacy_id",
      "projid",
      "title",
      "abstract",
      "investigator_display",
      "object",
      "observer",
      "date-obs",
      "procname",
      "velocity",
      "obstype",
      "veldef",
      "skyfreq",
      "restfreq",
      "ra",
      "dec",
      "pol",
      "band",
      "receiver",
      "backend",
      "bandwidth",
    ],
    :labels => {
      "telescope" => "Telescope",
      "proposal_id" => "Proposal ID",
      "legacy_id" => "Legacy ID",
      "projid" => "PROJID",
      "title" => "Title",
      "abstract" => "Abstract",
      "investigator_display" => "Investigators",
      "object" => "Object",
      "observer" => "Observer",
      "date-obs" => "Date Observed",
      "velocity" => "Velocity (km/s)",
      "veldef" => "Velocity Definition",
      "skyfreq" => "Sky Frequency (GHz)",
      "restfreq" => "Rest Frequency (GHz)",
      "ra" => "RA (J2000)",
      "dec" => "Dec (J2000)",
      "pol" => "Polarization",
      "bandwidth" => "Bandwidth (MHz)",
      "band" => "Band",
      "receiver" => "Receiver",
      "backend" => "Backend",
      "obstype" => "Observing Type",
      "procname" => "Procedure Name",
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

