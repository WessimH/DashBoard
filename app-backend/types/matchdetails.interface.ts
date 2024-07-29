export interface MatchDetails {
    // Team roles
    Team1Role1: string;
    Team1Role2: string;
    Team1Role3: string;
    Team1Role4: string;
    Team1Role5: string;
    Team2Role1: string;
    Team2Role2: string;
    Team2Role3: string;
    Team2Role4: string;
    Team2Role5: string;
  
    // Bans for each team
    Team1Ban1: string;
    Team1Ban2: string;
    Team1Ban3: string;
    Team1Ban4: string;
    Team1Ban5: string;
    Team2Ban1: string;
    Team2Ban2: string;
    Team2Ban3: string;
    Team2Ban4: string;
    Team2Ban5: string;
  
    // Picks for each team
    Team1Pick1: string;
    Team1Pick2: string;
    Team1Pick3: string;
    Team1Pick4: string;
    Team1Pick5: string;
    Team2Pick1: string;
    Team2Pick2: string;
    Team2Pick3: string;
    Team2Pick4: string;
    Team2Pick5: string;
  
    // Basic information
    Team1: string;
    Team2: string;
    Winner: number;  // Assuming Winner is an integer that denotes the winning team or other numeric value
    Team1Score: number;
    Team2Score: number;
  
    // Order of picks
    Team1PicksByRoleOrder: string;
    Team2PicksByRoleOrder: string;
  
    // Other details
    OverviewPage: string;
    Phase: string;
    UniqueLine: string;
    IsComplete: boolean;
    IsFilled: boolean;
    Tab: string;
  
    // Pagination information
    N_Page: number;
    N_TabInPage: number;
    N_MatchInPage: number;
    N_GameInPage: number;
    N_GameInMatch: number;
    N_MatchInTab: number;
    N_GameInTab: number;
  
    // Identifiers
    GameId: string;
    MatchId: string;
    GameID_Wiki: string;
  }
  