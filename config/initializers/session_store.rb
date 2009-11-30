# Be sure to restart your server when you modify this file.

# Your secret key for verifying cookie session data integrity.
# If you change this key, all old sessions will become invalid!
# Make sure the secret is at least 30 characters and all random, 
# no regular words or you'll be exposed to dictionary attacks.
ActionController::Base.session = {
  :key         => '_nrao-blacklight_session',
  :secret      => 'b8437d7cde318d64736e860eea604a4ad76f745d102bd621407d4442d789f740c2fff09667d4b9e6c54285623dabf24031a6dd0e6b7e6334e821cf5a7b72566c'
}

# Use the database for sessions instead of the cookie-based default,
# which shouldn't be used to store highly confidential information
# (create the session table with "rake db:sessions:create")
# ActionController::Base.session_store = :active_record_store
