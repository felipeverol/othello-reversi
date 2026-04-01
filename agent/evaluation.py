from game.utils import Player, Directions, Direction as d, BoardHouses as h

class Evaluation():
  __scoreBoard = [[h.CORNER, h.C, h.A, h.B, h.B, h.A, h.C, h.CORNER],
                [h.C, h.X, h.SIMPLE, h.SIMPLE, h.SIMPLE, h.SIMPLE, h.X, h.C],
                [h.A, h.SIMPLE, h.MIDDLE, h.MIDDLE, h.MIDDLE, h.MIDDLE, h.SIMPLE, h.A],
                [h.B, h.SIMPLE, h.MIDDLE, h.MIDDLE, h.MIDDLE, h.MIDDLE, h.SIMPLE, h.B],
                [h.B, h.SIMPLE, h.MIDDLE, h.MIDDLE, h.MIDDLE, h.MIDDLE, h.SIMPLE, h.B],
                [h.A, h.SIMPLE, h.MIDDLE, h.MIDDLE, h.MIDDLE, h.MIDDLE, h.SIMPLE, h.A],
                [h.C, h.X, h.SIMPLE, h.SIMPLE, h.SIMPLE, h.SIMPLE, h.X, h.C],
                [h.CORNER, h.C, h.A, h.B, h.B, h.A, h.C, h.CORNER]]

  __visited = [[False, False, False, False, False, False, False, False],
             [False, False, False, False, False, False, False, False],
             [False, False, False, False, False, False, False, False],
             [False, False, False, False, False, False, False, False],
             [False, False, False, False, False, False, False, False],
             [False, False, False, False, False, False, False, False],
             [False, False, False, False, False, False, False, False],
             [False, False, False, False, False, False, False, False]]

  __cornerExpansion = {
    d.NW: {"directions": [d.S, d.SE, d.E], "limits": [(0, 0), (3, 3)]},
    d.NE: {"directions": [d.S, d.SW, d.W], "limits": [(0, 4), (3, 7)]},
    d.SE: {"directions": [d.N, d.NW, d.W], "limits": [(4, 4), (7, 7)]},
    d.SW: {"directions": [d.N, d.NE, d.E], "limits": [(4, 0), (7, 3)]}
  }

  @staticmethod
  def abs(a):
    return a if a >= 0 else -a

  @staticmethod
  def normalize(a, b):
    return (a - b) / (Evaluation.abs(a) + Evaluation.abs(b) + 1)

  @staticmethod
  def hPositional(board: list[list[Player]], player: Player, totalPieces: int) -> float:
    positionalScore = 0
    for i in range(8):
      for j in range(8):
        if (board[i][j] == player):
          positionalScore += int(Evaluation.__scoreBoard[i][j].value)
          if (totalPieces < 20 and Evaluation.__scoreBoard[i][j] == h.MIDDLE):
            positionalScore += int(Evaluation.__scoreBoard[i][j].value) * 9

    return positionalScore

  @staticmethod
  def __initializeVisited():
    Evaluation.__visited = [[False, False, False, False, False, False, False, False],
                            [False, False, False, False, False, False, False, False],
                            [False, False, False, False, False, False, False, False],
                            [False, False, False, False, False, False, False, False],
                            [False, False, False, False, False, False, False, False],
                            [False, False, False, False, False, False, False, False],
                            [False, False, False, False, False, False, False, False],
                            [False, False, False, False, False, False, False, False]]

  @staticmethod
  def __expansion(curr: tuple[int, int], corner: d, board: list[list[Player]], player: Player) -> int:
    i, j = curr
    lowerLimit = Evaluation.__cornerExpansion[corner]["limits"][0]
    upperLimit = Evaluation.__cornerExpansion[corner]["limits"][1]
    if (i < lowerLimit[0] or i > upperLimit[0]): return 0
    if (j < lowerLimit[1] or j > upperLimit[1]): return 0
    if (Evaluation.__visited[i][j]): return 0

    Evaluation.__visited[i][j] = True
    if (board[i][j] != player): return 0

    expandDirections = Evaluation.__cornerExpansion[corner]["directions"]
    nextExpansions = Directions.nextPositions(curr, expandDirections)

    stability = 1
    stability += Evaluation.__expansion(nextExpansions[0], corner, board, player)
    stability += Evaluation.__expansion(nextExpansions[1], corner, board, player)
    stability += Evaluation.__expansion(nextExpansions[2], corner, board, player)
    return stability

  @staticmethod
  def hStability(board: list[list[Player]], player: Player) -> float:
    Evaluation.__initializeVisited()

    stabilityScore = 0

    stabilityScore += Evaluation.__expansion((0, 0), d.NW, board, player)
    stabilityScore += Evaluation.__expansion((0, 7), d.NE, board, player)
    stabilityScore += Evaluation.__expansion((7, 7), d.SE, board, player)
    stabilityScore += Evaluation.__expansion((7, 0), d.SW, board, player)

    return stabilityScore

  @staticmethod
  def hCorner(board: list[list[Player]], player: Player) -> float:
    corners = 0
    if (board[0][0] == player): corners += 1
    if (board[0][7] == player): corners += 1
    if (board[7][7] == player): corners += 1
    if (board[7][0] == player): corners += 1

    return corners

  @staticmethod
  def __neighbor(board: list[list[Player]], player: Player, i: int, j: int) -> bool:
    opponent = Player.BLACK if player == Player.WHITE else Player.WHITE
    rows = [i-1, i, i+1]
    cols = [j-1, j, j+1]

    for r in rows:
      for c in cols:
        if (r == i and c == j):
          continue

        if (r >= 0 and r < 8 and c >= 0 and c < 8):
          if (board[r][c] == opponent): return True
    
    return False


  @staticmethod
  def hLoud(board: list[list[Player]], player: Player) -> float:
    frontierPieces = 0
    for i in range(8):
      for j in range(8):
        if (board[i][j] == player):
          if (Evaluation.__neighbor(board, player, i, j)):
            frontierPieces += 1
            break

    return frontierPieces

  @staticmethod
  def hPieces(board: list[list[Player]], player: Player) -> float:
    playerPieces = 0
    for i in range(8):
      for j in range(8):
        if (board[i][j] == player):
          playerPieces += 1

    return playerPieces
