class AdvancedController < ApplicationController
  def index
    redirect_to :action => 'gbt'
  end

  def gbt
  end

  def submit
    q = ""
    keys = [:project, :i, :observer, :object, :band, :obstype, 
            :receiver, :backend, :procname]
    keys.each do |key|
      value = params[key]
      if value and not value.blank?
        q += " " + key.to_s + ":" + value.to_s
      end
    end
    q.strip!
    redirect_to :controller => 'catalog', :q => q
  end
end
