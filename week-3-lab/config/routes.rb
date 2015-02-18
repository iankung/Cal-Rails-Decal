Rails.application.routes.draw do

    root 'static_pages#home' 

    get '/about', to: 'static_pages#about' ##or use resources option

end
