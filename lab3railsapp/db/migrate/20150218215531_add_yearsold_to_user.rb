class AddYearsoldToUser < ActiveRecord::Migration
  def change
    add_column :users, :yearsold, :integer
  end
end
