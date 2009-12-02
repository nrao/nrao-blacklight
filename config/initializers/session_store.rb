# Be sure to restart your server when you modify this file.

# Your secret key for verifying cookie session data integrity.
# If you change this key, all old sessions will become invalid!
# Make sure the secret is at least 30 characters and all random, 
# no regular words or you'll be exposed to dictionary attacks.
ActionController::Base.session = {
  :key         => '_proposals_session',
  :secret      => '215de70ae6f51aff1e7c51cc11c5c7a2f02663ae8240c21c0656dbb426922a5b4985dd5d8e6a764a06642254cac834c655d025682906658b54a80c7adc0e8cc7'
}

# Use the database for sessions instead of the cookie-based default,
# which shouldn't be used to store highly confidential information
# (create the session table with "rake db:sessions:create")
# ActionController::Base.session_store = :active_record_store
