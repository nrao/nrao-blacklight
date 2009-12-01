# Be sure to restart your server when you modify this file.

# Your secret key for verifying cookie session data integrity.
# If you change this key, all old sessions will become invalid!
# Make sure the secret is at least 30 characters and all random, 
# no regular words or you'll be exposed to dictionary attacks.
ActionController::Base.session = {
  :key         => '_nrao-blacklight_session',
  :secret      => 'a60c3ec07058bae80b43f4977eb336c152306799ca45ca05b3a973d8a56c2c66ed41c77d1a57988a7cb30702c8740a29b6b334909f98542b6a91893e044061fc'
}

# Use the database for sessions instead of the cookie-based default,
# which shouldn't be used to store highly confidential information
# (create the session table with "rake db:sessions:create")
# ActionController::Base.session_store = :active_record_store
