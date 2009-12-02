# Be sure to restart your server when you modify this file.

# Your secret key for verifying cookie session data integrity.
# If you change this key, all old sessions will become invalid!
# Make sure the secret is at least 30 characters and all random, 
# no regular words or you'll be exposed to dictionary attacks.
ActionController::Base.session = {
  :key         => '_isstt_session',
  :secret      => '57c5a8ae52bbe9b6f9077dd9f2f65891312622f12d1919bdf97240aa07b950b1e8c7f68ddaf5417404e3d2f2f05a3d6e1a99b1aa1145721c53bf31ed92407eb1'
}

# Use the database for sessions instead of the cookie-based default,
# which shouldn't be used to store highly confidential information
# (create the session table with "rake db:sessions:create")
# ActionController::Base.session_store = :active_record_store
