# Be sure to restart your server when you modify this file.

# Your secret key for verifying cookie session data integrity.
# If you change this key, all old sessions will become invalid!
# Make sure the secret is at least 30 characters and all random, 
# no regular words or you'll be exposed to dictionary attacks.
ActionController::Base.session = {
  :key         => '_theses_session',
  :secret      => 'b5c7bd2ccf5a4b8ecd8d76d0fb4a19b74a6478c256678076dbdedc8f267ee5c2b83c5fc3d0e41b8d54b618ecb6be89577fe454f5bccae156264db2a472777b0b'
}

# Use the database for sessions instead of the cookie-based default,
# which shouldn't be used to store highly confidential information
# (create the session table with "rake db:sessions:create")
# ActionController::Base.session_store = :active_record_store
