class StaticPagesController < ApplicationController

  def home
  end

  def about
    @age = 17
    @major = 'stats'
  end

end
