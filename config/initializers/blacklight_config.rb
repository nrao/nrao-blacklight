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
      ["telescope_facet",
       "year_submitted",
       "type_facet",
       "joint_facet",]
    }
  }

  # default params for the SolrDocument.find_by_id method
  SolrDocument.default_params[:find_by_id] = {:qt => :document}

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
        "telescope_facet",
        "year_submitted",
        "type_facet",
        "joint_facet",
    ],
    :labels => {
        "telescope_facet"       => "Telescope",
        "year_submitted"        => "Year (Proposal Submitted)",
        "type_facet"            => "Proposal Type",
        "joint_facet"           => "Joint Proposal",
    }
  }

  # solr fields to be displayed in the index (search results) view
  #   The ordering of the field names is the order of the display
  config[:index_fields] = {
    :field_names => [
        "telescope",
        "prop_id",
        "legacy_id",
        "principal",
        "year_submitted",
        "type",
        "joint",
    ],
    :labels => {
        "telescope"             => "Telescope:",
        "prop_id"               => "Proposal ID:",
        "legacy_id"             => "Legacy ID:",
        "principal"             => "Principal Investigator:",
        "year_submitted"        => "Year:",
        "type"                  => "Proposal Type:",
        "joint"                 => "Joint Proposal:",
    }
  }

  # solr fields to be displayed in the show (single result) view
  #   The ordering of the field names is the order of the display
  config[:show_fields] = {
    :field_names => [
        "telescope",
        "prop_id",
        "legacy_id",
        "abstract",
        "principal",
        "investigator",
        "year_submitted",
        "type",
        "joint",
        "related",
    ],
    :labels => {
        "telescope"             => "Telescope:",
        "prop_id"               => "Proposal ID:",
        "legacy_id"             => "Legacy ID:",
        "abstract"              => "Abstract:",
        "principal"             => "Principal Investigator:",
        "investigator"          => "Investigators:",
        "year_submitted"        => "Year:",
        "type"                  => "Proposal Type:",
        "joint"                 => "Joint Proposal:",
        "related"               => "Related:",
    }
  }

  # "fielded" search select (pulldown)
  # label in pulldown is followed by the name of a SOLR request handler as
  # defined in solr/conf/solrconfig.xml
  config[:search_fields] ||= []
  config[:search_fields] << ['All Fields', 'search']

  # "sort results by" select (pulldown)
  # label in pulldown is followed by the name of the SOLR field to sort by and
  # whether the sort is ascending or descending (it must be asc or desc
  # except in the relevancy case).
  # label is key, solr field is value
  config[:sort_fields] ||= []
  config[:sort_fields] << ['relevance', '']
  config[:sort_fields] << ['Proposal ID, ascending', 'prop_id_sort asc']
  config[:sort_fields] << ['Proposal ID, descending', 'prop_id_sort desc']
  config[:sort_fields] << ['Year Submitted, ascending', 'year_sort asc']
  config[:sort_fields] << ['Year Submitted, descending', 'year_sort desc']

  # If there are more than this many search results, no spelling ("did you
  # mean") suggestion is offered.
  config[:spell_max] = 5
end

