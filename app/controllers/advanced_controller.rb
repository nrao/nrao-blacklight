class AdvancedController < ApplicationController
  def index
    redirect_to :action => 'gbt'
  end

  def gbt
    # redirect_to :controller => 'catalog', :q => 'i:balser'
  end
end
