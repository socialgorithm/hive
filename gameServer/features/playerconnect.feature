Feature: players can interact with the game server

  Background:
    Given the server is listening on localhost port 8081
    Given entity "tournamentServer" connects to "http://localhost:8081"

  Scenario: two players connect to the server
    Given entity "playerA" connects to "http://localhost:8081/?token=playerAToken"
    And entity "playerB" connects to "http://localhost:8081/?token=playerBToken"
    Then 2 players have connected
    And player with token "playerAToken" has connected
    And player with token "playerBToken" has connected

  Scenario: The tournamentServerConnects

