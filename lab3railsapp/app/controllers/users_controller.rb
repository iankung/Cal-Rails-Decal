class UsersController < ApplicationController
  def index
    @users = User.where("yearsold > ?", 50) 
  end

  def new
    @user = User.new
  end


  def show
  end

  def update
  end

  def edit
  end

  def create
    @user = User.new(user_params)
    if @user.save
      redirect_to users_path
    else
      render 'new'
    end
  end

  private
    def user_params
      params.require(:user).permit(:name, :yearsold)
    end

end
