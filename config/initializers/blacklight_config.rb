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
      []
    }
  }

  # default params for the SolrDocument.find_by_id method
  SolrDocument.default_params[:find_by_id] = {:qt => :document}

  config[:default_qt] = "search"

  # solr field values given special treatment in the show (single result) view
  config[:show] = {
    :html_title => "proposal_title",
    :heading => "proposal_title",
    :display_type => "format_code"
  }

  # solr fld values given special treatment in the index (search results) view
  config[:index] = {
    :show_link => "proposal_title",
    :num_per_page => 10,
    :record_display_type => "format_code"
  }

  # solr fields that will be treated as facets by the blacklight application
  #   The ordering of the field names is the order of the display
  config[:facet] = {
    :field_names => [
        "telescope_facet",
        "year_facet",
        "proposal_type_facet",
        "observing_type_facet",
        "rapid_response_type_facet",
        "joint_proposal_facet",
        "scientific_category_facet",
        "dissertation_plan_facet",
    ],
    :labels => {
        "telescope_facet"           => "Telescope",
        "year_facet"                => "Year (Submitted)",
        "proposal_type_facet"       => "Proposal Type",
        "observing_type_facet"      => "Observing Type",
        "rapid_response_type_facet" => "Rapid Response Type",
        "joint_proposal_facet"      => "Joint Proposal",
        "scientific_category_facet" => "Scientific Category",
        "dissertation_plan_facet"   => "Dissertation Plan",
    }
  }

  # solr fields to be displayed in the index (search results) view
  #   The ordering of the field names is the order of the display
  config[:index_fields] = {
    :field_names => [
        "principal_telescope",
        "proposal_id",
        "legacy_id",
        "principal_investigator",
        "year_submitted",
        "proposal_type",
        "joint_proposal",
    ],
    :labels => {
        "principal_telescope"    => "Telescope:",
        "proposal_id"            => "Proposal ID:",
        "legacy_id"              => "Legacy ID:",
        "abstract"               => "Abstract:",
        "principal_investigator" => "Principal Investigator:",
        "investigators"          => "Investigators:",
        "year_submitted"         => "Year:",
        "proposal_type"          => "Proposal Type:",
        "joint_proposal"         => "Joint Proposal:",
        "related_proposal"       => "Related:",
        "scientific_category"    => "Scientific Category:",
        "observing_type"         => "Observing Type:",
        "other_observing_type"   => "Other Observing Type:",
        "rapid_response_type"    => "Rapid Response Type:",
        "dissertation_plan"      => "Dissertation Plan:",
        "total_time"             => "Total Time:",
    }
  }

  # solr fields to be displayed in the show (single result) view
  #   The ordering of the field names is the order of the display
  config[:show_fields] = {
    :field_names => [
        "principal_telescope",
        "proposal_id",
        "legacy_id",
        "abstract",
        "principal_investigator",
        "investigators",
        "year_submitted",
        "scientific_category",
        "observing_type",
        "other_observing_type",
        "proposal_type",
        "rapid_response_type",
        "related_proposal",
        "joint_proposal",
        "dissertation_plan",
        "total_time",
    ],
    :labels => {
        "principal_telescope"    => "Telescope:",
        "proposal_id"            => "Proposal ID:",
        "legacy_id"              => "Legacy ID:",
        "abstract"               => "Abstract:",
        "principal_investigator" => "Principal Investigator:",
        "investigators"          => "Investigators:",
        "year_submitted"         => "Year:",
        "proposal_type"          => "Proposal Type:",
        "joint_proposal"         => "Joint Proposal:",
        "related_proposal"       => "Related:",
        "scientific_category"    => "Scientific Category:",
        "observing_type"         => "Observing Type:",
        "other_observing_type"   => "Other Observing Type:",
        "rapid_response_type"    => "Rapid Response Type:",
        "dissertation_plan"      => "Dissertation Plan:",
        "total_time"             => "Total Time:",
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
  config[:sort_fields] << ['Telescope, ascending', 'telescope_sort asc, score desc']
  config[:sort_fields] << ['Telescope, descending', 'telescope_sort desc, score desc']
  config[:sort_fields] << ['Proposal ID, ascending', 'proposal_id_sort asc']
  config[:sort_fields] << ['Proposal ID, descending', 'proposal_id_sort desc']
  config[:sort_fields] << ['Legacy ID, ascending', 'legacy_id_sort asc']
  config[:sort_fields] << ['Legacy ID, descending', 'legacy_id_sort desc']
  config[:sort_fields] << ['Year, ascending', 'date_sort asc, score desc']
  config[:sort_fields] << ['Year, descending', 'date_sort desc, score desc']

  # If there are more than this many search results, no spelling ("did you
  # mean") suggestion is offered.
  config[:spell_max] = 5
end

