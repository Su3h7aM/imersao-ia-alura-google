from rich.table import Table

from wsagent.services import get_msgs_by_limit


def print_top10(console, ws_data, limit_days):
    table = Table(title="Top 10 Usuários mais ativos")

    table.add_column("Rank", justify="center", style="red")
    table.add_column("Usuário", style="cyan")
    table.add_column("Mensagens", justify="center")
    table.add_column("Emoção", justify="center")

    _, user_count = get_msgs_by_limit(ws_data=ws_data, limit_days=limit_days)

    sorted_user_count = sorted(
        user_count.items(), key=lambda item: item[1], reverse=True
    )

    for rank, (user, count) in enumerate(sorted_user_count, start=1):
        rows = 0
        if rows <= 10:
            table.add_row(str(rank), user, str(count), "teste")
            rows += 1
    console.print(table)
