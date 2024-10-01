import sqlite3

class Database:
    def __init__(self, db_name='domains.db'):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS DISPOSABLE_DOMAINS (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                domain TEXT UNIQUE
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS PUBLIC_DOMAINS (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                domain TEXT UNIQUE
            )
        ''')
        self.conn.commit()

    def add_disposable_domain(self, domain):
        self._add_domains(domain, 'DISPOSABLE_DOMAINS')

    def add_public_domain(self, domain):
        self._add_domains(domain, 'PUBLIC_DOMAINS')

    def _add_domains(self, domain, table):
        if isinstance(domain, str):
            domain = [domain]  # Convert single domain string to a list

        unique_domains = set(domain)  # Use set to ensure uniqueness
        new_domains = []
        
        for d in unique_domains:
            if not self.is_domain_in_table(d, table):
                new_domains.append((d,))  # Prepare for bulk insert

        if new_domains:
            self.cursor.executemany(f'INSERT INTO {table} (domain) VALUES (?)', new_domains)
            self.conn.commit()

    def is_disposable_domain(self, domain):
        return self.is_domain_in_table(domain, 'DISPOSABLE_DOMAINS')

    def is_public_domain(self, domain):
        return self.is_domain_in_table(domain, 'PUBLIC_DOMAINS')

    def is_domain_in_table(self, domain, table):
        self.cursor.execute(f'SELECT 1 FROM {table} WHERE domain = ?', (domain,))
        return self.cursor.fetchone() is not None

    def remove_disposable_domain(self, domain):
        self.remove_domain(domain, 'DISPOSABLE_DOMAINS')

    def remove_public_domain(self, domain):
        self.remove_domain(domain, 'PUBLIC_DOMAINS')

    def remove_domain(self, domain, table):
        if self.is_domain_in_table(domain, table):
            self.cursor.execute(f'DELETE FROM {table} WHERE domain = ?', (domain,))
            self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()