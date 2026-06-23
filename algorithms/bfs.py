from collections import deque
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class BFS(BaseSearch):

    def search(self, initial: State) -> SearchResult:
        frontier = deque([initial])
        visited = {initial}
        nodes_expanded = 0
        nodes_generated = 1
        max_frontier_size = 1

        if initial.is_goal:
            return SearchResult(
                solution=initial,
                nodes_expanded=nodes_expanded,
                nodes_generated=nodes_generated,
                max_frontier_size=max_frontier_size,
                depth=initial.cost,
            )

        while frontier:
            state = frontier.popleft()
            nodes_expanded += 1

            for child in state.neighbors():
                if child in visited:
                    continue

                visited.add(child)
                nodes_generated += 1

                if child.is_goal:
                    return SearchResult(
                        solution=child,
                        nodes_expanded=nodes_expanded,
                        nodes_generated=nodes_generated,
                        max_frontier_size=max(max_frontier_size, len(frontier)),
                        depth=child.cost,
                    )

                frontier.append(child)
                max_frontier_size = max(max_frontier_size, len(frontier))

        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
            depth=0,
        )
