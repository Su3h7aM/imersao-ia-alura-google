from rich.table import Table

from wsagent.services import get_msgs_by_limit


def print_top10(console, ws_data, limit_days):
    table = Table(title="Top 10 Usuários mais ativos")

    table.add_column("Rank", justify="center", style="red")
    table.add_column("Usuário", style="cyan")
    table.add_column("Mensagens", justify="center")
    # table.add_column("Emoção", justify="center")

    _, users_count = get_msgs_by_limit(ws_data=ws_data, limit_days=limit_days)

    ranked = rank_list(raw_list=users_count, limit=10, index=1)

    for rank, (user, count) in enumerate(ranked):
        table.add_row(str(rank), user, str(count))

    console.print(table)


def rank_list(raw_list, limit, index: int):
    sorted_list = sorted(raw_list.items(), key=lambda item: item[index], reverse=True)

    ranked = {}
    for rank, (user, count) in enumerate(sorted_list, start=1):
        if rank <= limit:
            if user not in ranked:
                ranked[user] = 0
            ranked[user] = count

    return ranked.items()
