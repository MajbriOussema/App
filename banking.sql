
CREATE TABLE IF NOT EXISTS `accounts` (
  `id` int(11) DEFAULT NULL,
  `iban` varchar(32) DEFAULT NULL,
  `username` varchar(20) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `amount` int(11) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

ALTER TABLE `accounts`
  ADD PRIMARY KEY (`id`);


ALTER TABLE `accounts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=0;

CREATE TABLE IF NOT EXISTS `transactions` (
  `id` int(11) DEFAULT NULL,
  `receiver_iban` varchar(32) DEFAULT NULL,
  `sender_id` int(11) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `amount` int(11) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
  
ALTER TABLE `transactions`
  ADD PRIMARY KEY (`id`),
  ADD CONSTRAINT sender_id FOREIGN KEY (sender_id) REFERENCES accounts(id);
  ;

ALTER TABLE `transactions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=0;