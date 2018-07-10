
require "timeout"
require "socket"

# the default timeout for the possibly time consuming actions
DEFAULT_TIMEOUT = 15

# set the application introspection port for communication
def set_port
  # 14155 is currently an unassigned port
  ENV["YUI_HTTP_PORT"] ||= "14155"
  ENV["YUI_HTTP_PORT"]
end

# is the target port open?
# @param host [Integer] the host to connect to
# @param port [Integer] the port number
# @return [Boolean] true if the port is open, false otherwise
def port_open?(host, port)
  TCPSocket.new(host, port).close
  true
rescue Errno::ECONNREFUSED, Errno::EHOSTUNREACH
  false
end

# wait until the specified port is open or until the timeout is reached
# @param host [Integer] the host to connect to
# @param port [Integer] the port number
# @raise Timeout::Error when the port is not opened in time
def wait_for_port(host, port)
  Timeout.timeout(DEFAULT_TIMEOUT) do
    loop do
      sleep(1)
      puts "Waiting for #{host}:#{port}..."
      break if port_open?(host, port)
    end
  end
end

# start the application in background
# @param application [String] the command to start
def start_app(application)
  @app_host = "localhost"
  @app_port = set_port
  # create a new process group so we can easily kill it will all subprocesses
  @app_pid = spawn(application, pgroup: true)
  wait_for_port(@app_host, @app_port)
end

Given(/^I start the "(.*)" application$/) do |application|
  start_app(application)
end

Then(/^I wait for the application to finish(?: for up to (\d+) seconds)?$/) do |seconds|
  timeout = seconds.to_i
  timeout = DEFAULT_TIMEOUT if timeout == 0

  Timeout.timeout(timeout) do
    Process.wait(@app_pid)
  end
end