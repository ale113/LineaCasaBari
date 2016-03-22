#!/usr/bin/perl -w

use CGI qw(:standard);
use CGI::Cookie;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use strict;
use Template;
use CGI::Session;
use XML::LibXML;

my $cgi=new CGI;
print $cgi->header('text/html');
my $session = CGI::Session->load();
my $email=$session->param("email");

my $parser=XML::LibXML->new;
my $doc=$parser->parse_file("../data/Prodotti.xml");
my $template=Template->new({
		INCLUDE_PATH => '../public_html/temp',
	});
my $cod;
if ($ENV{'REQUEST_METHOD'} eq 'POST')
{
	$cod=param("codice");
	
}
else
{
	$cod=$ENV{'QUERY_STRING'};
}
my $messaggio="false";
my @cod_prodotti=$doc->findnodes("Prodotti/Prodotto/Codice/text()");

if(@cod_prodotti)
{
	if($cod)
	{
		my $i;
		foreach $i (@cod_prodotti)
		{
			if($i ne $cod)
			{
				$messaggio="il codice inserito non corrisponde a nessun prodotto esistente";
			}
			else
			{
				$messaggio="false";
				last;
			}
		}
	}
	else
	{
		$messaggio="inserisci un codice per la ricerca";
	}
}
else
{
	$messaggio="non ci sono prodotti";
}
my $vars;

if($messaggio eq "false")
{
	push my @prodotto, $doc->findnodes("Prodotti/Prodotto[Codice='$cod']/Codice/text()");
	push @prodotto, $doc->findnodes("Prodotti/Prodotto[Codice='$cod']/Nome/text()");
	push @prodotto, $doc->findnodes("Prodotti/Prodotto[Codice='$cod']/Descrizione/text()");
	push @prodotto, $doc->findnodes("Prodotti/Prodotto[Codice='$cod']/Categoria/text()");
	push @prodotto, $doc->findnodes("Prodotti/Prodotto[Codice='$cod']/Prezzo/text()");
	push @prodotto, $doc->findnodes("Prodotti/Prodotto[Codice='$cod']/Data_aggiunta/text()");
	push @prodotto, $doc->findnodes("Prodotti/Prodotto[Codice='$cod']/Valutazione/text()");
	push @prodotto, $doc->findnodes("Prodotti/Prodotto[Codice='$cod']/Immagine/text()");
	my $num_tag=$doc->findvalue("count(Prodotti/Prodotto[Codice='$cod']/Tag)");
	for(my $x=0; $x<$num_tag;$x++)
	{
		push @prodotto, $doc->findnodes("Prodotti/Prodotto[Codice='$cod']/Tag/text()");
	}
	push @prodotto, $doc->findnodes("Prodotti/Prodotto[Codice='$cod']/Recensione/Titolo/text()");
	push @prodotto, $doc->findnodes("Prodotti/Prodotto[Codice='$cod']/Recensione/Nome_visualizzato/text()");
	push @prodotto, $doc->findnodes("Prodotti/Prodotto[Codice='$cod']/Recensione/Data_pubblicazione/text()");
	push @prodotto, $doc->findnodes("Prodotti/Prodotto[Codice='$cod']/Recensione/Testo/text()");
	push @prodotto, $doc->findnodes("Prodotti/Prodotto[Codice='$cod']/Recensione/Voto_prodotto/text()");
	push @prodotto, $doc->findnodes("Prodotti/Prodotto[Codice='$cod']/Recensione/Voto_recensione/text()");
	
	my @label = ('Codice','Nome','Descrizione','Categoria','Prezzo','Data aggiunta','Valutazione','Immagine');
	for(my $x=0; $x<$num_tag;$x++)
	{
		push @label, "Tag";
	}
	push @label, "Titolo recensione", "Nome ", " Data"," Testo", "Voto Prodotto", " Voto recensione";

	my $y=0;
	my $tot='<form action="modifica_prodotti.cgi" method="post"';
	for(my $i=0; $i<8;$i++)
	{
		my $x='<li class="gestione-block"><label class="gestione-labels">'."@label[$i]: </label>".'<div class="inputLeft"></div><div class="gestione-inputMiddle"><input class="input" name='."@label[$i]".'type="text" value='."@prodotto[$y]".'/></div><div class="inputRight"></div></li>';
		$y++;
		$tot=$tot.$x;
	}
	my $counter=1;
	for(my $i=0; $i<$num_tag;$i++)
	{
		my $x='<li class="gestione-block"><label class="gestione-labels">'."@label[$i]: </label>".'<div class="inputLeft"></div><div class="gestione-inputMiddle"><input class="input" name='."@label[$i]".' type="text" value='."@prodotto[$y]".'/></div><div class="inputRight"></div></li>';
		$y++;
		$counter++;
		$tot=$tot.$x;
	}
	for(my $i=0; $i<6;$i++)
	{
		my $x='<li class="gestione-block"><label class="gestione-labels">'."@label[$i]: </label>".'<div class="inputLeft"></div><div class="gestione-inputMiddle"><input class="input" name='."@label[$i]".' type="text" value='."@prodotto[$y]".'/></div><div class="inputRight"></div></li>';
		$y++;
		$tot=$tot.$x;
	}

	$y=0;
	$tot=$tot.'<li class="gestione-block"><div class="gestione-button_block"><button class="button" type="submit">modifica</button><input type="hidden" name="prodotto" value="'."$cod".'"/></form><form action="togli_prodotto.cgi" method="post"><input type="hidden" name="prodotto" value="'."$cod".'"/><button class="button" type="submit">togli prodotto</button></form></div></li>';
	my $lista_prodotto='<ul class="gestione-aggiungi_form">'."$tot"."</ul>";
	$vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => "true",
		'list' => "true",
		'lista_prodotti' => $lista_prodotto,
		'pagina' => "rimuovi_modifica",
	};
}
else
{
	$vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => "true",
		'list' => "false",
		'messaggio' => $messaggio,
		'pagina' => "rimuovi_modifica",
		
		
	};
}
my $file='gestione_prodotti_temp.html';
$template->process($file,$vars) || die $template->error();
