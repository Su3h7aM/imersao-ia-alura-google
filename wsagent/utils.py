from rich.table import Table

from wsagent.services import get_msgs_by_limit


def print_top10(console, ws_data, limit_days):
    table = Table(title="Top 10 Usuários mais ativos")

    table.add_column("Rank", justify="center", style="red")
    table.add_column("Usuário", style="cyan")
    table.add_column("Mensagens", justify="center")
    table.add_column("Emoção", justify="center")

    _, users_count = get_msgs_by_limit(ws_data=ws_data, limit_days=limit_days)

    sorted_users_count = sorted(
        users_count.items(), key=lambda item: item[1], reverse=True
    )

    for rank, (user, count) in enumerate(sorted_users_count, start=1):
        if rank <= 10:
            table.add_row(str(rank), user, str(count), "teste")

    console.print(table)


def rank_list(list, limit):
    sorted_list = sorted(list.items(), key=lambda item: item[1], reverse=True)

    for rank, (user, count) in enumerate(sorted_list, start=1):
        if rank <= limit:
            table.add_row(str(rank), user, str(count), "teste")
